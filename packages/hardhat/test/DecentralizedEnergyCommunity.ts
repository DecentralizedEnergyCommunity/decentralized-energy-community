import { expect } from "chai";
import { ethers } from "hardhat";
import { ZeroAddress } from "ethers";
import { DecentralizedEnergyCommunity, SampleERC20 } from "../typechain-types";
import { SignerWithAddress } from "@nomicfoundation/hardhat-ethers/signers";
import { anyValue } from "@nomicfoundation/hardhat-chai-matchers/withArgs";

describe("DecentralizedEnergyCommunity", function () {
  // We define a fixture to reuse the same setup in every test.

  let decentralizedEnergyCommunity: DecentralizedEnergyCommunity;
  let sampleERC20: SampleERC20;
  let owner: SignerWithAddress;
  let addr1: SignerWithAddress;
  before(async () => {
    [owner, addr1] = await ethers.getSigners();

    // Mock to represent a EURC token
    const totalSupply = ethers.parseUnits("100000", 6);
    const sampleERC20ContractFactory = await ethers.getContractFactory("SampleERC20");
    sampleERC20 = (await sampleERC20ContractFactory.deploy("Sample, ERC20", "SERC20", 6, totalSupply)) as SampleERC20;
    await sampleERC20.waitForDeployment();

    // Make sure addr1 has some tokens
    const transferAmount = ethers.parseUnits("10000", 6);
    await sampleERC20.connect(owner).transfer(addr1.address, transferAmount);

    const decentralizedEnergyCommunityContractFactory = await ethers.getContractFactory("DecentralizedEnergyCommunity");
    decentralizedEnergyCommunity = (await decentralizedEnergyCommunityContractFactory.deploy(
      owner.address,
      await sampleERC20.getAddress(),
    )) as DecentralizedEnergyCommunity;
    await decentralizedEnergyCommunity.waitForDeployment();
  });

  describe("Deployment", function () {
    context("Happy Path Test Cases", function () {
      it("Should return the correct token address", async function () {
        expect(await decentralizedEnergyCommunity.token()).to.equal(await sampleERC20.getAddress());
      });

      it("Should correctly grant default admin role", async function () {
        const defaultAdminRole = await decentralizedEnergyCommunity.DEFAULT_ADMIN_ROLE();
        expect(await decentralizedEnergyCommunity.hasRole(defaultAdminRole, owner.address)).to.be.true;
      });
    });

    context("Error Test Cases", function () {
      it("Should revert if the default admin address is the zero address", async function () {
        const decentralizedEnergyCommunityContractFactory = await ethers.getContractFactory(
          "DecentralizedEnergyCommunity",
        );
        await expect(
          decentralizedEnergyCommunityContractFactory.deploy(ZeroAddress, await sampleERC20.getAddress()),
        ).to.be.revertedWith("Invalid default admin address");
      });

      it("Should revert if the token address is the zero address", async function () {
        const decentralizedEnergyCommunityContractFactory = await ethers.getContractFactory(
          "DecentralizedEnergyCommunity",
        );
        await expect(decentralizedEnergyCommunityContractFactory.deploy(owner.address, ZeroAddress)).to.be.revertedWith(
          "Invalid token address",
        );
      });
    });
  });

  describe("createCommunity", function () {
    context("Happy Path Test Cases", function () {
      it("Should create a community", async function () {
        // Generate hashed EAN codes
        const salt = ethers.randomBytes(32);
        const ean1 = 123456789;
        const ean2 = 987654321;

        const hashedEan1 = await decentralizedEnergyCommunity.generateHash(ean1, salt);
        const hashedEan2 = await decentralizedEnergyCommunity.generateHash(ean2, salt);

        // Prepare meters array
        const meters = [
          { meterType: 1, meterEAN: hashedEan1 }, // Assuming 1 is PRODUCER
          { meterType: 2, meterEAN: hashedEan2 }, // Assuming 2 is CONSUMER
        ];

        // Set escrow amount
        const escrowAmount = ethers.parseUnits("100", await sampleERC20.decimals());

        // Mint tokens to address and Approve token transfer
        await sampleERC20.connect(addr1).approve(await decentralizedEnergyCommunity.getAddress(), escrowAmount);

        // Call createCommunity
        await expect(decentralizedEnergyCommunity.connect(addr1).createCommunity(meters, escrowAmount))
          .to.emit(decentralizedEnergyCommunity, "CommunityCreated")
          .withArgs(1n, addr1.address, anyValue, escrowAmount);

        // Verify community creation
        const communityId = await decentralizedEnergyCommunity.participantAddressToCommunity(addr1.address);
        expect(communityId).to.equal(1n);

        const community = await decentralizedEnergyCommunity.communities(1);
        expect(community.active).to.be.false;
        expect(community.participantCount).to.equal(1);

        // Verify balance update
        const balance = await decentralizedEnergyCommunity.balances(addr1.address);
        expect(balance).to.equal(escrowAmount);
      });
    });
  });
});
