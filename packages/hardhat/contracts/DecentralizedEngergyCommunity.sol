//SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

import { IDecentralizedEnergyCommunity } from "./IDecentralizedEnergyCommunity.sol";
import { AccessControl } from "@openzeppelin/contracts/access/AccessControlEnumerable.sol";
import { IERC20Metadata } from "@openzeppelin/contracts/token/ERC20/extensions/IERC20Metadata.sol";
import { SafeERC20 } from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

/**
 * @title   DecentralizedEnergyCommunity
 * @notice  This contract is the main contract for the Decentralized Energy Community
 */
contract DecentralizedEnergyCommunity is
	IDecentralizedEnergyCommunity,
	AccessControl
{
	using SafeERC20 for IERC20Metadata;

	bytes32 public constant SETTLEMENT_ADMIN_ROLE =
		keccak256("SETTLEMENT_ADMIN_ROLE");
	uint256 public constant MAX_PARTICIPANTES_PER_COMMUNITY = 100;
	uint256 public constant MAX_SETTLEMENTS = 100;
	uint256 public immutable minEscrowAmount;

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
		minEscrowAmount = 100 * (10 ** IERC20Metadata(_token).decimals()); //100 in token decimals
	}

	function createCommunity(
		Meter[] calldata _meters,
		uint256 _escrowAmount
	) external override {
		require(
			_meters.length > 0 && _meters.length <= 4,
			"Invalid number of meters"
		);

		// User should have approved this contract to transfer the escrow amount
		IERC20Metadata(token).safeTransferFrom(
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

		emit CommunityCreated(communityId, msg.sender, _meters, _escrowAmount);
	}

	function joinCommunity(
		uint32 _communityId,
		Meter[] calldata _meters,
		uint256 _escrowAmount
	) external override {
		require(
			_meters.length > 0 && _meters.length <= 4,
			"Invalid number of meters"
		);

		require(
			participantAddressToCommunity[msg.sender] == 0,
			"Participant already in a community"
		);

		// User should have approved this contract to transfer the escrow amount
		IERC20Metadata(token).safeTransferFrom(
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

		emit CommunityJoined(_communityId, msg.sender, _meters, _escrowAmount);
	}

	function addMeterToParticipant(
		uint32 _communityId,
		uint32 _participantIndex,
		Meter calldata _newMeter
	) external override {
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

		emit MeterAddedToParticipant(
			_communityId,
			_participantIndex,
			_newMeter
		);
	}

	/**
	 * @notice  Seetle the balances of the participants in the community
	 * @param   _settlements The settlements to be updated
	 */
	function settleCommunityBalances(
		ParticipantSettlement[] calldata _settlements
	) external override onlyRole(SETTLEMENT_ADMIN_ROLE) {
		ParticipantSettlement memory settlement;
		uint256 totalAmountEarned = 0;
		uint256 totalAmountPaid = 0;
		require(_settlements.length <= MAX_SETTLEMENTS, "Too many settlements");

		// Add up total amount earned and total amount paid for the settlement period
		for (uint32 i = 0; i < _settlements.length; i++) {
			settlement = _settlements[i];
			totalAmountEarned += settlement.amountEarned;
			totalAmountPaid += settlement.amountPaid;
		}
		// Check if the total amount earned is equal to the total amount paid for the settlement period.
		// We can't create money out of thin air.
		require(
			totalAmountEarned == totalAmountPaid,
			"Amount paid not equal to amount earned"
		);

		for (uint32 i = 0; i < _settlements.length; i++) {
			settlement = _settlements[i];
			Community storage community = communities[settlement.communityId];
			Participant storage participant = community.participants[
				settlement.participantIndex
			];
			uint256 participantBalance = balances[participant.wallet];
			balances[participant.wallet] =
				participantBalance +
				settlement.amountEarned -
				settlement.amountPaid;

			uint256 tokenUnit = 10 ** IERC20Metadata(token).decimals();

			if (participantBalance < minEscrowAmount) {
				// If the balance is less than the minimum escrow amount, the participant is set to inactive
				participant.active = false;
			} else {
				participant.active = true;
			}
		}

		emit CommunityBalancesSettled(_settlements);
	}

	function withdraw(uint256 _amount) external override {
		require(
			balances[msg.sender] - minEscrowAmount >= _amount,
			"Insufficient balance to withdraw"
		);
		uint256 amountToWithdraw;
		uint256 currentBalance = balances[msg.sender];
		if (currentBalance - _amount >= minEscrowAmount) {
			amountToWithdraw = _amount;
		} else {
			amountToWithdraw = _amount - minEscrowAmount;
		}
		balances[msg.sender] -= amountToWithdraw;
		IERC20Metadata(token).safeTransfer(msg.sender, amountToWithdraw);
		emit AmountWithdrawn(msg.sender, amountToWithdraw);
	}

	function communityIsActive(
		uint32 _communityId
	) external view override returns (bool) {
		Community storage community = communities[_communityId];
		return community.active;
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
	) external view override returns (bytes32 generatedHash) {
		require(salt != bytes32(0), "Invalid salt");
		return keccak256(abi.encodePacked(address(this), value, salt));
	}
}
