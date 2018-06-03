# Caldav neuron for Kalliope

## Synopsis

Get / Create / Search for event in your caldav agenda.

## Installation

**This neuron is not even in alpha mode yet. Try only after reading the code and sample file to understand how it works.**

  ```
  kalliope install --git-url https://github.com/bacardi55/kalliope-kaldav.git
  ```

## Options

| parameter   | required | default            | choices | comment                                                                                                                     |
|-------------|----------|--------------------|---------|-----------------------------------------------------------------------------------------------------------------------------|
| url         | yes      |                    | String  | The URL of your caldav. It can be http://login:pass@url of agenda                                                           |
| action      | yes      |                    | String  | list, create, search,                                                                                                       |
| max_results | no       |                    | Integer | Number of results when using list or search action                                                                          |
| name        | no       |                    | String  | The name of the event to create (only when action is create)                                                                |
| start_date  | no       |                    | String  | Used for event creation (event start date/time) or search/list (event after this date)                                      |
| end_date    | no       |                    | String  | Used for event creation (event end date/time) or search/list (event not after this date)                                    |
| timezone    | no       |                    | String  | Your locale (eg: 'Europe/Paris')                                                                                            |
| date_format | no       | '%b %d %Y %I:%M%p' | String  | Date format to map the pattern in dates (start/end) strings (default format map the following string: 'Jun 1 2005  1:33PM') |



## Return Values

| Name    | Description       | Type   | sample                                 |
|---------|-------------------|--------|----------------------------------------|
| actions | The action used   | string | The used action (create, list, search) |
| events  | A list of events. | list   |                                        |


## Synapses example

Look into [sample folder](samples) as this is not fixed yet.


* [Blog post about this neuron](http://bacardi55.org/2017/01/09/kalliope-neuron-for-google-calendar.html)
* [my posts about kalliope](http://bacardi55.org/kalliope.html)
