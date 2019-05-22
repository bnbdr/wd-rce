WD My Cloud RCE PoC Exploit
-------------------------
Tested on *`WD My Cloud EX2 Ultra`* versions **2.31.149** and **2.31.163**.
Should work on other MyCloud models.

for the write-up go [here](https://bnbdr.github.io/posts/wd/).

Authentication bypass to acquire user-session ([CVE-2019-9950](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-9950)) 
---------------------
- `login_mgr.cgi` matches credentials against `/etc/shadow`, therefore the `"nobody"` account can be used to gain a low-privilege user session by  providing "nobody"'s **default, empty password**.


Root-RCE using low-privilege session ([CVE-2019-9949](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-9949))
-------------------------------------------------------
1. `cgi-bin/webfile_mgr.cgi` allows an attacker in the same network to perform  **command injection** by abusing the `"name"` parameter to the `cgi_unzip` command.

1. `cgi-bin/webfile_mgr.cgi` allows an attacker in the same network to issue the `cgi_untar` command on a user-controlled archive to create a persistent **symbolic link on the filesystem** which **can be written** into by issuing the command again.


Unauthenticated file upload ([CVE-2019-9951](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-9951)) 
---------------------------
The page `web/jquery/uploader/uploadify.php` can be accesses without any credentials and allows **uploading arbitrary files** to any location on the attached storage under either:
* `/mnt/HD`
* `/mnt/USB`
* `/mnt/isoMount`

________


Disclosure timeline
-------------------

- **2019-01-20** 🍄 reported to [psirt@wdc.com](mailto:psirt@wdc.com) with 30-day deadline
- **2019-01-22** `ᴡᴅ` sent an automated(?) response 
- **2019-02-05** 🍄 requested comfirmation of issues
- **2019-02-06** `ᴡᴅ` asked for 90 days to fix the issues
- **2019-03-05** 🍄 requested status update
- **2019-03-15** `ᴡᴅ` asked for *additional* 90-day extension
- **2019-03-16** 🍄 agreed on 30-day extension
- **2019-03-27** `ᴡᴅ` *released first patch (CVE-2019-9950, CVE-2019-9951)*
- **2019-05-20** `ᴡᴅ` *release of second patch (CVE-2019-9949)*
- **2019-05-22** 🍄 public disclosure
