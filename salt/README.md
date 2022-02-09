# Salt

What is salt and how it is typically used to protect hashed data?

A new salt is randomly generated for each password. Typically, the salt and the password (or its version after key stretching) are concatenated and fed to a cryptographic hash function, and the output hash value (but not the original password) is stored with the salt in a database. Hashing allows later authentication without keeping and therefore risking exposure of the plaintext password if the authentication data store is compromised. Note that due to this, salts don't need to be encrypted or stored separately from the hashed password itself, because even if an attacker has access to the database with the hash values and the salts, the correct use of said salts will hinder common attacks.

Example case:

You are going to publish a website visit history data for research purposes.
There are IP addresses in the data and these are sensitive information.

Problem:

Personal information must be replaced with ids which do not reveal the original information.
Simple hash(IP_address) is not protecting the IP addresses.
Reason is that attacker can calculate hash with all possible IP addresses.
After that the attacker could reveal the IP address which was used to create the hash.

Solution:

Use a random nonsense string called salt which is added to the IP address data.
After preparation nobody knows the salt value and thus cannot reveal the IP_address + salt.
As a result, each unique IP address has new unique ID based on hash but this ID does not reveal the IP address.

# Hash + salt example

```sh
python3 salt.py
```
