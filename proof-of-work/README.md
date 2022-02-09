# Proof-of-work

Example case:

Mining means looking a hash value according to the difficulty set by the Bitcoin network.
Difficulty means the pattern which must be in the beginning of the hash value.

Block contains the transactions and a pointer to the previous block + nonsense.

Example message is "A new block of transactions  and pointer to the previous block. + Nonsense:".
Then proof-of-work is finding a message + nonsense string which hash256 begins with 00000.

00000105e324521c216017d63461225e53daf2b22b11af39ef35e0ea2822e237
Found a hash which starts with 00000
Nonsense is khXNjlf9LMdp

A new block of transactions  and pointer to the previous block. + Nonsense: khXNjlf9LMdp

# Proof-of-work search

```sh
python3 work.py
```
