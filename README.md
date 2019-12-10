# Automated Classroom PDF Attachment Downloader
_"auto" download classroom post attachments_


## have you ever wanted to automatically download the pdf of the day's lesson that one teacher put up on classroom because you're too lazy and can't afford to click a couple of buttons but if you express your discontent about this specific issue to that teacher then you'd be worried that he/she/it would be less prone to like you for the rest of the school year?

oddly specific, but for me y̵̡̝̼̝͖̤̞̹̻̜͆̉͒͘͘͜è̷͍̫̝̞̱̠͖̤̄̑̏̓̎͑͂̇̽̏̍͘s̸̡̬̹̣̰̤͔̰͔͕̤̟͊̔̓̾̌̋͂̒̐͘͝ͅ.


# BUT...

now, all you have to do is clone this repo, run __app.py__ (after going thru prerequisites), and relax as one python script takes care of it (ikr how anti-climatic).

---
## Prerequisites
1. Run the following on terminal (or not whatever I'm not your dad)

```
$ pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

$ pip install PyDrive
```
2. Clone this repo

3. Go onto https://developers.google.com/classroom/quickstart/python and follow *only* Step 1. You should get a download of a file `credentials.json`

4. Put `credentials.json` next to `app.py`

5. Run `app.py`. The first time, it'll ask you for a lot of google authentication and all of that jazz. __MAKE SURE THAT YOU SIGN IN WITH YOUR SCHOOL GOOGLE ACCOUNT__

6. (For now) Enter the `id` of the classroom (no, not class invite code). _This is the tricky part that probably should've gotten more documentation, but I'm in progress of making a selection ui that'll let you choose which class. For now, refer to google's classroom api documentation to figure this out._

7. enjoy


