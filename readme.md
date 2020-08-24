# SalVatioN
- **Author:** LIU-Yinyi
- **Date:** Aug 24, 2020
- **Version:** 0.1.0 - Beta & Hung Up
- **Abstract:** An open-source subversion gui client desktop software based on PyQt5. Note: See also the announcements in the last section.

## Motivations
Why I started this project was an interesting episode.

> This project was originally for Yinyi's Macbook because at that time MacOSX Catalina didn't have relevant softwares that could support free subversion client desktop version. But the lab duty required svn so I wrote a gui version as *SALVATION*. It happened that the word **salvation** has the letter **svn**, as a result, I named the software as this name. :D


## Quickstarts

### For Developer
If you would like to run from source codes and revised as you like, you could follow the instructions as below:

```bash
# install the subversion
sudo apt-get install subversion     /** For Debian Linux **/
brew install subversion             /** For Mac OSX **/

# install the dependent libraries
pip install -r requirements.txt

# run the applicaton
python main.py
```

### For Common Users
Download the compiled packages in Release with selecting the corresponding OS.


## Usages
The gui of software was designed as simple as possible.
  
> <u>The *philosophy* is that find the potenials with your **mouse-click**</u>,     
> both `single/double left click` as well as `right click`.

The gif will be shown in the following parts.

### Step 1: Configure Bundles
This part shows you how to add the configuration to bundle list.

![step1.gif]()

### Step 2: Connect Remote Repositories
This part shows you how to view and operate with the remote svn repositories after connected.

![step2.gif]()

### Step 3: Modify Local Repositories
This part shows you how to deal with the local repositories after checkout.

![step3.gif]()

### Step 4: Manage Version Control
This part shows you how to manage with version control.

![step4.gif]()


## Acknowledges
SalVatioN is powered by @LIU-Yinyi (C) 2020

## Announcements
I found that SalVatioN just covered what I needed within our lab duties, while it still lacks a lot of features that svn once designed. Also I just persuaded my professor replaced svn with git + onedrive. Nothing would bother me :D

As a result, the priority of maintaining this project is no longer high. But I will optimize it if I have spare time in the future. Anyway, coding for SalVatioN helped me startup on Qt5. If you would like to use `svn+ssh` method to have a glance on svn repository, the functions have already covered. Now it lacks of the abilities of local submissions as well as version control.

Thanks for reviewing my awkward codes :D

