# Unity Catalog UI
## Not required but recommended for confirming things are up and running and persistent.
1. Clone the unity catalog oss repo (https://github.com/unitycatalog/unitycatalog.git)
2. Navigate to the ui directory, open Dockerfile in vscode and change from crlf to lf
3. Docker build -t -imagename- .
4. Docker save -o imagename.tar:imagename
5. cp this tar to somewhere your vm can access
6. load the tar
- may need to modify the conf files as well to be lf, as of this git commit a warning stated they would be converted to crlf if touched by git