# Simhash

Example case:

You want your web service users to change their passwords.
Web service cannot save the plain text password.
Instead, service stores sha256 hashes of the passwords users are using.
You can easily make sure that users are selecting a new password.
As the hash changes if the user changes the password you can make sure the old one is not reused.

Problem:
You would like prevent users from changing the existing password just few characters.
I.e. If password is myG00Doldphrase user cannot set the new password as myG00DoldphrasE11.

Solution:
SimHash is a technique for quickly estimating how similar two passwords are.
In addition to sha256 you can save simhash of the password a user is using.
Then you can compare a new password against the simhash and estimate the similarity.

# Simhash usage

```python
from simhash_password_test import distance, simhash_value

random_salt = 'TsvJQrGOHf7uZya7w9BPsu42iB1tqYzJHendCV'

original_password_hash = simhash_value('mypassword' + random_salt)

new_hash = simhash_value('mypassword1' + random_salt)
print(new_hash)
print('Distance is %d' % distance(original_password_hash, new_hash))

new_hash = simhash_value('mynewpassword123' + random_salt)
print(new_hash)
print('Distance is %d' % distance(original_password_hash, new_hash))

```

# Password similarity check test

```sh
python3 simhash_password_test.py
```
