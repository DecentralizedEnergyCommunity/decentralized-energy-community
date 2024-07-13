//SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

import { AccessControl } from "@openzeppelin/contracts/access/AccessControlEnumerable.sol";
import { IERC20 } from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import { SafeERC20 } from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

/**
 * @title   DecentralizedEnergyCommunity
 * @notice  This contract is the main contract for the Decentralized Energy Community
 */
contract DecentralizedEnergyCommunity is AccessControl {
	using SafeERC20 for IERC20;

	struct Community {
		uint32 id;
		bool active;
		bool hasProducer;
		uint32 participantCount;
		mapping(uint32 => Participant) participants;
	}

	struct Participant {
		uint32 index; // index in community's participants mapping
		uint32 meterCount;
		address wallet;
		bool active;
		mapping(uint32 => Meter) meters;
	}

	struct ParticipantSettlement {
		address wallet;
		uint256 amountEarned;
		uint256 amountPaid;
	}

	struct Meter {
		MeterType meterType;
		bytes32 meterEAN; // hashed EAN code
	}

	enum MeterType {
		NONE,
		PRODUCER,
		CONSUMER
	}

	uint256 public constant MAX_PARTICIPANTES_PER_COMMUNITY = 100;
	uint256 public constant MAX_SETTLEMENTS = 100;

	uint32 public communityIds;
	address public token;
	mapping(uint32 => Community) public communities;
	mapping(address => uint32) public participantAddressToCommunity;
	mapping(bytes32 => bool) public existingMeters;
	mapping(address => uint256) public balances;

	/**
	 * @notice  Constructor of the contract
	 * @param   _defaultAdmin This address will have the `DEFAULT_ADMIN_ROLE`
	 * @param   _token The address of the token contract that will be used for escrow and settlement
	 */
	constructor(address _defaultAdmin, address _token) {
		_setupRole(DEFAULT_ADMIN_ROLE, _defaultAdmin);
		token = _token;
	}

	function createCommunity(
		Meter[] calldata _meters,
		uint256 _escrowAmount
	) external {
		require(
			_meters.length > 0 && _meters.length <= 4,
			"Invalid number of meters"
		);

		// User should have approved this contract to transfer the escrow amount
		IERC20(token).safeTransferFrom(
			msg.sender,
			address(this),
			_escrowAmount
		);
		balances[msg.sender] += _escrowAmount;

		uint32 communityId = communityIds++;

		Community storage newCommunity = communities[communityId];
		newCommunity.id = communityId;
		newCommunity.active = false;
		newCommunity.participantCount = 1;

		Participant storage newParticipant = newCommunity.participants[0];
		newParticipant.index = newCommunity.participantCount;
		newParticipant.wallet = msg.sender;
		newParticipant.meterCount = uint32(_meters.length);

		bool hasProducer = false;
		for (uint32 i = 0; i < _meters.length; i++) {
			require(
				_meters[i].meterType != MeterType.NONE,
				"Invalid meter type"
			);
			require(
				!existingMeters[_meters[i].meterEAN],
				"Meter with this EAN already exists"
			);
			newParticipant.meters[i] = _meters[i];
			if (_meters[i].meterType == MeterType.PRODUCER) {
				hasProducer = true;
			}
		}

		newCommunity.hasProducer = hasProducer;
		participantAddressToCommunity[msg.sender] = communityId;
	}

	function joinCommunity(
		uint32 _communityId,
		Meter[] calldata _meters,
		uint256 _escrowAmount
	) external {
		require(
			_meters.length > 0 && _meters.length <= 4,
			"Invalid number of meters"
		);

		require(
			participantAddressToCommunity[msg.sender] == 0,
			"Participant already in a community"
		);

		// User should have approved this contract to transfer the escrow amount
		IERC20(token).safeTransferFrom(
			msg.sender,
			address(this),
			_escrowAmount
		);
		balances[msg.sender] += _escrowAmount;

		Community storage newCommunity = communities[_communityId];
		uint32 participantCount = ++newCommunity.participantCount;
		require(
			participantCount <= MAX_PARTICIPANTES_PER_COMMUNITY,
			"Community is full"
		);

		newCommunity.participantCount = participantCount;

		Participant storage newParticipant = newCommunity.participants[
			participantCount - 1
		];
		newParticipant.index = newCommunity.participantCount;
		newParticipant.wallet = msg.sender;
		newParticipant.meterCount = uint32(_meters.length);

		bool hasProducer = false;
		bool active = false;
		for (uint32 i = 0; i < _meters.length; i++) {
			require(
				_meters[i].meterType != MeterType.NONE,
				"Invalid meter type"
			);
			require(
				!existingMeters[_meters[i].meterEAN],
				"Meter with this EAN already exists"
			);
			newParticipant.meters[i] = _meters[i];
			if (_meters[i].meterType == MeterType.PRODUCER) {
				hasProducer = true;
			} else if (_meters[i].meterType == MeterType.CONSUMER) {
				if (hasProducer) {
					active = true;
				}
			}
		}

		newCommunity.hasProducer = hasProducer;
		newCommunity.active = active;
		participantAddressToCommunity[msg.sender] = _communityId;
	}

	function communityIsActive(uint32 _communityId) public view returns (bool) {
		Community storage community = communities[_communityId];
		return community.active;
	}

	function addMeterToParticipant(
		uint32 _communityId,
		uint32 _participantIndex,
		Meter calldata _newMeter
	) external {
		Community storage community = communities[_communityId];
		Participant storage participant = community.participants[
			_participantIndex
		];

		require(
			participant.meterCount < 4,
			"Participant already has maximum number of meters"
		);

		require(
			participantAddressToCommunity[msg.sender] == 0,
			"Participant already in a community"
		);

		require(_newMeter.meterType != MeterType.NONE, "Invalid meter type");
		require(
			!existingMeters[_newMeter.meterEAN],
			"Meter with this EAN already exists"
		);

		participant.meters[participant.meterCount] = _newMeter;
		participant.meterCount++;

		bool hasProducer = false;
		bool active = false;

		if (_newMeter.meterType == MeterType.PRODUCER) {
			hasProducer = true;
		} else if (_newMeter.meterType == MeterType.CONSUMER) {
			if (hasProducer) {
				active = true;
			}
		}
	}

	/**
	 * @notice Generate hash of a value using the value, a salt, and the current contract address
	 * @dev This function is used to generate a hash of the meter EAN code
	 * @param value - the player's address
	 * @param salt the player's salt
	 * @return generatedHash the hashed data
	 */
	function generateHash(
		uint256 value,
		bytes32 salt
	) public view returns (bytes32 generatedHash) {
		require(salt != bytes32(0), "Invalid salt");
		return keccak256(abi.encodePacked(address(this), value, salt));
	}
}
