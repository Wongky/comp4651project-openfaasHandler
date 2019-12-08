FROM python:3

#######
# Allows you to add additional self packages via build-arg
# put to python path
ARG ADDITIONAL_PACKAGE_FOLDERNAME
#######

#######
# Allows you to add additional folder via build-arg
# folder need to copy to cwd of running function
# dont user "function", "python", "darknet"
ARG ADDITIONAL_FILE_FOLDERNAME
#######

#app running current directory
ARG VAR_CWD=/home/app

#python path (dont change)
ARG VAR_PYTHON=${VAR_CWD}/python

RUN curl -sSL https://github.com/openfaas/faas/releases/download/0.13.0/fwatchdog > /usr/bin/fwatchdog \
    && chmod +x /usr/bin/fwatchdog

# Add non root user
RUN addgroup --system app && adduser --system --group app 

WORKDIR ${VAR_CWD}/

COPY index.py           .
COPY requirements.txt   .

RUN chown -R app ${VAR_CWD} && \
  mkdir -p ${VAR_PYTHON} && chown -R app ${VAR_CWD}
USER app
ENV PATH=$PATH:${VAR_CWD}/.local/bin:${VAR_PYTHON}/bin/
ENV PYTHONPATH=$PYTHONPATH:${VAR_PYTHON}
RUN pip install -r requirements.txt --target=${VAR_PYTHON}

RUN mkdir -p function
RUN touch ./function/__init__.py
WORKDIR ${VAR_CWD}/function/
COPY function/requirements.txt	.
RUN pip install -r requirements.txt --target=${VAR_PYTHON}

WORKDIR ${VAR_CWD}/
USER root

######get darknet file
RUN mkdir -p darknet
WORKDIR ${VAR_CWD}/darknet
RUN wget -q https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names && wget -q https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg && wget -q https://pjreddie.com/media/files/yolov3.weights
#######

WORKDIR ${VAR_CWD}/
COPY function           function

#############use package in function
RUN if [ "x$ADDITIONAL_PACKAGE_FOLDERNAME" = "x" ] ; then echo Argument ADDITIONAL_PACKAGE_FOLDERNAME not provided ; else mv "function/$ADDITIONAL_PACKAGE_FOLDERNAME" "python/$ADDITIONAL_PACKAGE_FOLDERNAME" ; fi
#############
#############copy file to cwd
RUN if [ "x$ADDITIONAL_FILE_FOLDERNAME" = "x" ] ; then echo Argument ADDITIONAL_FILE_FOLDERNAME not provided ; else mv "function/$ADDITIONAL_FILE_FOLDERNAME" "$ADDITIONAL_FILE_FOLDERNAME" ; fi
##############

WORKDIR ${VAR_CWD}/
RUN chown -R app:app ./ && \
  chmod -R 777 ${VAR_PYTHON}
USER app

ENV fprocess="python3 index.py"

HEALTHCHECK --interval=1s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
