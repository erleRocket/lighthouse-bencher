# Google Lighthouse Bencher
Dev by the Performance War Team at https://www.reezocar.com

This application, automates Google Lighthouse tests of your website to track the evolution of the important "loading time" metrics in your seo optimization.

![https://www.reezocar.com Speed Index SEO optimization](https://github.com/erleRocket/lighthouse-bencher/blob/master/SEO-optim-win.png)

## humans behind this app
- #DEVOPS : devops@reezocar.com (Ludovic Pichon)
- #DEV #SEO : erle@reezocar.com (Erlé Alberton)
- #CTO @Reezocar (Vincent Deboeuf)

## requirements
- a free acount in https://logz.io/
- docker App Linux and python environment

*Pre requirements*

- python 3
- npm & nodeJS

*Installation*

- `pip install python-gtmetrix`
- `npm install -g lighthouse`
- `pip install matplotlib==3.0.3`
- `pip install numpy==1.16.2`
- `pip install pandas==0.24.1`
- `pip install python-dateutil==2.6.0`
- `pip install requests==2.14.2`
- `pip install seaborn==0.9.0`
- `pip install tqdm==4.31.1`

## step by step
- update the urlConfig.json with your URLs
- create an app to exec the test.sh script with a cron tab
- create a cron tab push the data to your logz.io account
- import LightHouse Dashboard config (json)
- follow your metrics

