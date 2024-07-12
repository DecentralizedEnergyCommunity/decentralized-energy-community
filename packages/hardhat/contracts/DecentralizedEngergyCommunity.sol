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
		Participant[] participants;
	}

	struct Participant {
		uint32 id;
		address wallet;
		Meter[4] meters;
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

	mapping(uint256 => Community) public communities;

	/**
	 * @notice  Constructor of the contract
	 * @param   _defaultAdmin This address will have the `DEFAULT_ADMIN_ROLE`
	 */
	constructor(address _defaultAdmin) {
		_setupRole(DEFAULT_ADMIN_ROLE, _defaultAdmin);
	}

	function createCommunity(Participant[] calldata _participants) external {
		require(
			_participants.length > 0 && _participants.length <= 100,
			"Invalid number of participants"
		);

		// Community is not active until there is at leaste one producer and one consumer
		Community storage community = communities[++communityIds];
		community.id = communityIds;

		// Add the participants to the community
		for (uint256 i = 0; i < _participants.length; i++) {
			Participant memory participant = _participants[i];
			community.participants.push(_participants[i]);
			// loop through particpant meters
			if (participant.meters.length > 0) {
				// loop through particpant meters
				for (uint256 j = 0; j < participant.meters.length; j++) {
					Meter memory meter = participant.meters[j];
					if (meter.meterType == MeterType.PRODUCER) {
						community.hasProducer = true;
					}
					if (
						meter.meterType == MeterType.CONSUMER &&
						community.hasProducer
					) {
						community.active = true;
					}
				}
			}
		}

		// Add the community to the storage
		communities[community.id] = community;
	}

	function addParticipantsToCommunity(
		uint256 _communityId,
		Participant[] calldata _participants
	) external {
		require(
			_participants.length > 0 && _participants.length <= 100,
			"Invalid number of participants"
		);
		Community storage community = communities[_communityId];

		// Add the participants to the community
		for (uint256 i = 0; i < _participants.length; i++) {
			Participant memory participant = _participants[i];
			community.participants.push(_participants[i]);

			if (participant.meters.length > 0) {
				// loop through particpant meters
				for (uint256 j = 0; j < participant.meters.length; j++) {
					Meter memory meter = participant.meters[j];
					if (meter.meterType == MeterType.PRODUCER) {
						community.hasProducer = true;
					}
					if (
						meter.meterType == MeterType.CONSUMER &&
						community.hasProducer
					) {
						community.active = true;
					}
				}
			}
		}
	}
}
