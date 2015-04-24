FROM ubuntu
MAINTAINER Matthew Fournier <mfournier.ca>

# install dependancies
RUN apt-get update
RUN apt-get install --yes git r-base r-base-dev

RUN R -e "install.packages(c('ggplot2', 'shiny', 'dplyr', 'ggplot-themes'), repos='http://cran.us.r-project.org')"

# install the application
RUN git clone --recursive http://github.com/mfournierca/code2015.git /usr/local/code2015
RUN cd /usr/local/code2015 && git fetch origin docker && git checkout docker

EXPOSE 3729

RUN R -e "shiny::runApp('/usr/local/code2015/shiny', port=3729)"
