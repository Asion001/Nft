// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "OpenZeppelin/openzeppelin-contracts@4.4.0/contracts/token/ERC721/ERC721.sol";

contract nft is ERC721 {
    uint256 tokenCounter;

    constructor(string memory _name, string memory _symbol)
        ERC721(_name, _symbol)
    {
        tokenCounter = 0;
    }
}
