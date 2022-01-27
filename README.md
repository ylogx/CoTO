CoTO
====

Covid TO - Toronto & Ontario COVID-19 vaccine appointment booking website automation.

The purpose of this project is to reduce the headache of filling out all the information to see if the vaccine slots
are available or not.


## Installation
To setup, ensure firefox selenium runtime is installed. Use selenium to figure out the installation steps.

To setup the python requirements, run:

```bash
make install
```


## Run
Before running the application, use the template file by running `cp .env.tpl .env`.
Fill your required details in the `.env` file. These will be used to fill field on the appointment website.

To run the automation for booking a new appointment slot, use:

```bash
make run
```
