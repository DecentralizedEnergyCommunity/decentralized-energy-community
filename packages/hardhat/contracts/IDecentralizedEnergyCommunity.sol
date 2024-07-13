// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

interface IDecentralizedEnergyCommunity {
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
		uint32 communityId;
		uint32 participantIndex;
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

	event CommunityCreated(
		uint32 indexed communityId,
		address indexed creator,
		Meter[] meters,
		uint256 escrowAmount
	);

	event CommunityJoined(
		uint32 indexed communityId,
		address indexed participant,
		Meter[] meters,
		uint256 escrowAmount
	);

	event MeterAddedToParticipant(
		uint32 indexed communityId,
		uint32 indexed participantIndex,
		Meter meter
	);

	event CommunityBalancesSettled(ParticipantSettlement[] settlements);
	event AmountWithdrawn(address indexed participant, uint256 amount);

	function SETTLEMENT_ADMIN_ROLE() external view returns (bytes32);
	function MAX_PARTICIPANTES_PER_COMMUNITY() external view returns (uint256);
	function MAX_SETTLEMENTS() external view returns (uint256);

	function minEscrowAmount() external view returns (uint256);
	function communityIds() external view returns (uint32);
	function token() external view returns (address);
	function communities(
		uint32
	) external view returns (uint32, bool, bool, uint32);
	function participantAddressToCommunity(
		address
	) external view returns (uint32);
	function existingMeters(bytes32) external view returns (bool);
	function balances(address) external view returns (uint256);

	function createCommunity(
		Meter[] calldata _meters,
		uint256 _escrowAmount
	) external;
	function joinCommunity(
		uint32 _communityId,
		Meter[] calldata _meters,
		uint256 _escrowAmount
	) external;
	function communityIsActive(
		uint32 _communityId
	) external view returns (bool);
	function addMeterToParticipant(
		uint32 _communityId,
		uint32 _participantIndex,
		Meter calldata _newMeter
	) external;
	function settleCommunityBalances(
		ParticipantSettlement[] calldata _settlements
	) external;
	function withdraw(uint256 _amount) external;
	function generateHash(
		uint256 value,
		bytes32 salt
	) external view returns (bytes32 generatedHash);
}
