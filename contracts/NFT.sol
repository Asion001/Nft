// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "OpenZeppelin/openzeppelin-contracts@4.4.0/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract nft is ERC721URIStorage {
    address private owner;
    uint256 private tokenCounter;

    constructor(string memory _name, string memory _symbol)
        ERC721(_name, _symbol)
    {
        owner = msg.sender;
        tokenCounter = 0;
    }

    function addToken(address _to, string memory _tokenURI) public {
        require(msg.sender == owner);
        _mint(_to, tokenCounter);
        _setTokenURI(tokenCounter, _tokenURI);
        tokenCounter += 1;
    }
}
