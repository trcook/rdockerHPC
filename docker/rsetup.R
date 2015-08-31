packages<-c(
"devtools",
"RCurl",
"MatchIt",
"Zelig"
)

for(i in packages){
	install.packages(i)
}

require('devtools')
install_github(repo="trcook/tmisc",subdir="tmisc")