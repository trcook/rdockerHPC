packages<-c(
"devtools",
"RCurl",
"MatchIt",
"Zelig",
"doRedis"
)


install.packages(packages)

require('devtools')
install_github(repo="trcook/tmisc",subdir="tmisc")
install_github(repo='bwlewis/doRedis')