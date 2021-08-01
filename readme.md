## SastSearch

A web-app that could search information powered by Django.

SAST Homework.

### Register and Login

**Register**

A verification email will immediately be sent to the mail address after the form is submitted.

And then the account would turn into a "pending" status.

Accounts in this status would:

+ When registered again with the same password, a new verification email will be sent.
+ When registered again with different passwords, it will prompt that the address is taken.

If you forget your password, please jump to `/login` page and click 'Forgot Password', and then follow the steps.

If you lost your verification email, please register with the same email address and password again.

Please note that only the latest verification email under a certain address is valid, and the email will expire in 10 minutes.

**Login**

Avatar: using Gravatar to provide for user's avatar.


*By c7w*


