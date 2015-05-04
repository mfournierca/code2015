FROM rocker/r-base
MAINTAINER Matthew Fournier <mfournier.ca>

# install dependancies
RUN apt-get update
RUN apt-get install --yes git r-base r-base-dev

RUN R -e "install.packages('ggplot2', repos='http://cran.us.r-project.org')"
RUN R -e "install.packages('dplyr', repos='http://cran.us.r-project.org')"
RUN R -e "install.packages('shiny', repos='http://cran.us.r-project.org')"

# install the application
RUN git clone --recursive http://github.com/mfournierca/code2015.git /usr/local/code2015
RUN cd /usr/local/code2015 && git fetch origin master && git checkout master

EXPOSE 5000

CMD ["R", "-e", "shiny::runApp('/usr/local/code2015/shiny', port=5000, host='0.0.0.0')"]
