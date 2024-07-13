//SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

import { AccessControl } from "@openzeppelin/contracts/access/AccessControlEnumerable.sol";
import { IERC20 } from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/**
 * @title   DecentralizedEnergyCommunity
 * @notice  This contract is the main contract for the Decentralized Energy Community
 */
contract DecentralizedEnergyCommunity is AccessControl {
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

	struct Meter {
		MeterType meterType;
		bytes32 meterEAN; // hashed EAN code
	}

	enum MeterType {
		NONE,
		PRODUCER,
		CONSUMER
	}

	uint32 public communityIds;
	mapping(uint32 => Community) public communities;
	mapping(address => uint32) public participantAddressToCommunity;

	/**
	 * @notice  Constructor of the contract
	 * @param   _defaultAdmin This address will have the `DEFAULT_ADMIN_ROLE`
	 */
	constructor(address _defaultAdmin) {
		_setupRole(DEFAULT_ADMIN_ROLE, _defaultAdmin);
	}

	function createCommunity(Meter[] calldata _meters) external {
		require(
			_meters.length > 0 && _meters.length <= 4,
			"Invalid number of meters"
		);

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
			newParticipant.meters[i] = _meters[i];
			if (_meters[i].meterType == MeterType.PRODUCER) {
				hasProducer = true;
			}
		}

		newCommunity.hasProducer = hasProducer;
		participantAddressToCommunity[msg.sender] = communityId;
	}

	function joindCommunity(
		uint32 _communityId,
		Meter[] calldata _meters
	) external {
		require(
			_meters.length > 0 && _meters.length <= 4,
			"Invalid number of meters"
		);

		require(
			participantAddressToCommunity[msg.sender] == 0,
			"Participant already in a community"
		);

		Community storage newCommunity = communities[_communityId];
		uint32 participantCount = ++newCommunity.participantCount;
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
}
