//SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

import { AccessControl } from "@openzeppelin/contracts/access/AccessControlEnumerable.sol";

/**
 * @title   DecentralizedEnergyCommunity
 * @notice  This contract is the main contract for the Decentralized Energy Community
 */
contract DecentralizedEnergyCommunity is AccessControl {
	struct Community {
		uint32 id;
		bool active;
		bool hasProducer;
		bool hasConsumer;
		uint32 participantCount;
		mapping(uint32 => Participant) participants;
	}

	struct Participant {
		uint32 id;
		address wallet;
		uint32 meterCount;
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
	uint32 public participantIds;
	mapping(uint32 => Community) public communities;

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
		uint32 participantId = participantIds++;

		Community storage newCommunity = communities[communityId];
		newCommunity.id = communityId;
		newCommunity.active = true;
		newCommunity.participantCount = 1;

		Participant storage newParticipant = newCommunity.participants[0];
		newParticipant.id = participantId;
		newParticipant.wallet = msg.sender;
		newParticipant.meterCount = uint32(_meters.length);

		bool hasProducer = false;
		bool hasConsumer = false;
		for (uint32 i = 0; i < _meters.length; i++) {
			newParticipant.meters[i] = _meters[i];
			if (_meters[i].meterType == MeterType.PRODUCER) {
				hasProducer = true;
			} else if (_meters[i].meterType == MeterType.CONSUMER) {
				hasConsumer = true;
			}
		}

		newCommunity.hasProducer = hasProducer;
		newCommunity.hasConsumer = hasConsumer;
	}

	function communityHasProducerAndConsumer(
		uint32 _communityId
	) public view returns (bool) {
		Community storage community = communities[_communityId];
		return community.hasProducer && community.hasConsumer;
	}

	function addMeterToParticipant(
		uint32 _communityId,
		uint32 _participantId,
		Meter calldata _newMeter
	) external {
		Community storage community = communities[_communityId];
		Participant storage participant = community.participants[
			_participantId
		];

		require(
			participant.meterCount < 4,
			"Participant already has maximum number of meters"
		);

		participant.meters[participant.meterCount] = _newMeter;
		participant.meterCount++;

		if (_newMeter.meterType == MeterType.PRODUCER) {
			community.hasProducer = true;
		} else if (_newMeter.meterType == MeterType.CONSUMER) {
			community.hasConsumer = true;
		}
	}
}
