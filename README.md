# SQLIFinder

A Light Weight Tool for checking Local File Inclusion (SQLI) vulnerabilities by replacing sqli payloads in the parameters values and checking 'sql error' in the response.

## Installation
```
git clone https://github.com/rix4uni/SQLIFinder.git
cd SQLIFinder
#pip3 install -r requirements.txt
```

## Example usages

Note: must use `uro`

Single URL:
```
echo "http://testphp.vulnweb.com/showimage.php?file=./pictures/1.jpg" | python3 sqlifinder.py
```

Multiple URLs:
```
cat sqli-urls.txt | python3 sqlifinder.py
```

urls.txt contains:
```
http://testphp.vulnweb.com:80/AJAX/infocateg.php?id='
http://testphp.vulnweb.com:80/bxss/vuln.php?id='
http://testphp.vulnweb.com:80/listproducts.php?cat='
http://testphp.vulnweb.com/artists.php?artist='
http://testphp.vulnweb.com/listproducts.php?id='
http://testphp.vulnweb.com/Mod_Rewrite_Shop/details.php?id="
```

output:
```
VULNERABLE [MySQL]: http://testphp.vulnweb.com:80/AJAX/infocateg.php?id='
VULNERABLE [MySQL]: http://testphp.vulnweb.com:80/bxss/vuln.php?id='
VULNERABLE [MySQL]: http://testphp.vulnweb.com:80/listproducts.php?cat='
VULNERABLE [MySQL]: http://testphp.vulnweb.com/artists.php?artist='
VULNERABLE [MySQL]: http://testphp.vulnweb.com/listproducts.php?id='
VULNERABLE [MySQL]: http://testphp.vulnweb.com/Mod_Rewrite_Shop/details.php?id="
```

## Chaining With Other Tools
```
echo "http://testphp.vulnweb.com" | waybackurls | gf sqli | uro | anew | python3 sqlifinder.py
echo "http://testphp.vulnweb.com" | waybackurls | gf sqli | uro | anew sqli-urls.txt # use this output in Multiple URLs
```