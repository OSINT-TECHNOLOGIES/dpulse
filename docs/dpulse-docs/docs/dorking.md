# Automatic Google Dorking scan mode

Automatic Google Dorking scan is an extended domain research function with prepared Google Dorking databases for different purposes. 

## Prepared Dorking databases description

At the moment DPULSE offers the following prepared databases for automatic Google Dorking:

1. IoT dorking
2. Files dorking
3. Admin panels dorking
4. Web elements dorking

IoT dorking table contains following 20 dorks:
```
inurl:":8080" site:{}
inurl:":1883" site:{}
inurl:":8883" site:{}
inurl:":554" site:{}
inurl:":81" site:{}
inurl:":5000" site:{}
inurl:":9000" site:{}
inurl:":10000" site:{}
inurl:debug site:{}
inurl:device site:{}
inurl:control site:{}
inurl:status site:{}
inurl:service site:{}
inurl:monitor site:{}
inurl:stream site:{}
inurl:video site:{}
inurl:camera site:{}
inurl:sensor site:{}
inurl:api site:{}
inurl:firmware site:{}
```

Files dorking table contains following 30 dorks:
```
filetype:pdf site:{}
filetype:doc site:{}
filetype:docx site:{}
filetype:xlsx site:{}
filetype:xls site:{}
filetype:ppt site:{}
filetype:pptx site:{}
filetype:txt site:{}
filetype:csv site:{}
filetype:xml site:{}
filetype:json site:{}
filetype:html site:{}
filetype:php site:{}
filetype:asp site:{}
filetype:aspx site:{}
filetype:js site:{}
filetype:css site:{}
filetype:jpg site:{}
filetype:jpeg site:{}
filetype:png site:{}
filetype:gif site:{}
filetype:mp3 site:{}
filetype:mp4 site:{}
filetype:avi site:{}
filetype:zip site:{}
filetype:rar site:{}
filetype:sql site:{}
filetype:db site:{}
filetype:conf site:{}
filetype:ini site:{}
```

Admin panels dorking table contains following 72 dorks:
```
site:{} intitle:"WordPress Login"
site:{} inurl:/wp-admin/
site:{} intext:"Войти в WordPress"
site:{} intitle:"Dashboard" "WordPress"
site:{} intitle:"Joomla! Administrator Login"
site:{} inurl:/administrator/
site:{} intitle:"Joomla! 3.x" "Login"
site:{} intitle:"Drupal login"
site:{} inurl:/user/login
site:{} intitle:"Drupal 8" "Login"
site:{} intitle:"phpMyAdmin"
site:{} inurl:/phpmyadmin/
site:{} intitle:"phpMyAdmin 4.x"
site:{} intitle:"Magento Admin"
site:{} inurl:/admin/
site:{} intitle:"Magento 2" "Admin"
site:{} intitle:"vBulletin Admin CP"
site:{} inurl:/admincp/
site:{} intitle:"vBulletin 4.x" "Admin"
site:{} intitle:"osCommerce Administration"
site:{} intitle:"osCommerce 2.x" "Admin"
site:{} intitle:"PrestaShop Back Office"
site:{} inurl:/admin-dev/
site:{} intitle:"PrestaShop 1.7" "Back Office"
site:{} intitle:"OpenCart Admin Panel"
site:{} intitle:"OpenCart 3.x" "Admin"
site:{} intitle:"Zen Cart Admin"
site:{} intitle:"Zen Cart 1.5" "Admin"
site:{} intitle:"MediaWiki" "Special:UserLogin"
site:{} inurl:/mediawiki/index.php/Special:UserLogin
site:{} intitle:"Moodle" "Log in to the site"
site:{} inurl:/login/index.php
site:{} intitle:"Concrete5" "Sign In"
site:{} inurl:/index.php/dashboard/
site:{} intitle:"TYPO3" "Backend Login"
site:{} inurl:/typo3/
site:{} intitle:"Plone" "Log in"
site:{} inurl:/login_form
site:{} intitle:"Django" "Site administration"
site:{} inurl:/rails/admin/
site:{} intitle:"Ruby on Rails" "Admin"
site:{} intitle:"Craft CMS" "Control Panel"
site:{} inurl:/admin/
site:{} intitle:"ExpressionEngine" "Control Panel"
site:{} inurl:/admin.php
site:{} intitle:"Kentico" "CMS Desk"
site:{} inurl:/cmsdesk/
site:{} intitle:"Umbraco" "Backoffice"
site:{} inurl:/umbraco/
site:{} intitle:"Sitecore" "Launchpad"
site:{} inurl:/sitecore/
site:{} intitle:"DotNetNuke" "Host"
site:{} inurl:/host/
site:{} intitle:"SharePoint" "Sign In"
site:{} inurl:/_layouts/15/
site:{} intitle:"Plesk" "Login"
site:{} inurl:login.php?user=admin
site:{} inurl:dashboard
site:{} intitle:"admin login"
site:{} intitle:"administrator login"
site:{} "admin panel"
site:{} inurl:panel
site:{} inurl:cp
site:{} inurl:controlpanel
site:{} inurl:backend
site:{} inurl:management
site:{} inurl:administration
site:{} intitle:"admin access"
site:{} intitle:"control panel"
site:{} "admin login" +directory
site:{} "administrator login" +password
site:{} inurl:/plesk-login/
```

Web elements dorking table contains following 25 dorks:
```
site:{} intext:"index of"
site:{} inurl:admin
site:{} inurl:login
site:{} inurl:dashboard
site:{} inurl:wp-content
site:{} inurl:backup
site:{} inurl:old
site:{} inurl:temp
site:{} inurl:upload
site:{} inurl:download
site:{} inurl:config
site:{} inurl:setup
site:{} inurl:install
site:{} inurl:database
site:{} inurl:log
site:{} inurl:debug
site:{} inurl:api
site:{} inurl:secret
site:{} inurl:private
site:{} inurl:secure
site:{} inurl:password
site:{} inurl:auth
site:{} inurl:token
site:{} inurl:session
site:{} inurl:panel
```

## Creating custom Dorking database

DPULSE allows you to create your own custom Google Dorking database. You can do it using DPULSE CLI by selecting menus as shown below:

![dorking_start](https://github.com/user-attachments/assets/fc8fe1ba-1845-46d1-a9b9-d09d3dc03ce6)

After you select this menu point you will be welcomed with custom Dorking DB generator. It's very simple to use. First you should enter your new custom Dorking DB name without any extensions. Then you'll be prompted to enter id of your first dork (first id in custom DB is always 1, and every next dork gives +1 to id) and dork itself. There's a rule DPULSE requires from you when inputting dorks: when it comes to define domain in dork, put {} instead of it so the program code will replace these brackets with actual domain you'll enter lately.

Example of custom Dorking DB generator interaction is shown below:

![customdork](https://github.com/user-attachments/assets/8f3e8ca5-feec-4bf5-add8-048f54931b67)

In result, new .db file will appear in dorking folder, which can be selected later to use in scan:

![dorking_customdbresult](https://github.com/user-attachments/assets/0cd4facc-215b-4e56-ab56-aa23cb5136db)

And how it looks inside:

![look_inside](https://github.com/user-attachments/assets/023467c2-008b-451f-8e14-88b7e54a8c3c)



