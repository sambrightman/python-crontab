
Bug Reports and Development
===========================

Please report any problems to the `github issues tracker <https://github.com/doctormo/python-crontab/issues>`_. Please use Git and push patches to the `github project code hosting <https://github.com/doctormo/python-crontab>`_.

**Note:** If you get the error ``TypeError: __init__() takes exactly 2 arguments`` when using CronTab, you have the wrong module installed. You need to install ``python-crontab`` and not ``crontab`` from pypi or your local package manager and try again.


Description
===========

Crontab module for read and writing crontab files and accessing the system cron
automatically and simply using a direct API.

Comparing the `below chart <http://en.wikipedia.org/wiki/Cron#CRON_expression>`_
you will note that W, L, # and ? symbols are not supported as they are not
standard Linux or SystemV crontab format.

|Field Name   |Mandatory  |Allowed Values   |Special Characters |Extra Values |
|-------------|-----------|-----------------|-------------------|-------------|
|Minutes      |Yes        |0-59             |\* / , -           | < >         |
|Hours        |Yes        |0-23             |\* / , -           | < >         |
|Day of month |Yes        |1-31             |\* / , -           | < >         |
|Month        |Yes        |1-12 or JAN-DEC  |\* / , -           | < >         |
|Day of week  |Yes        |0-6 or SUN-SAT   |\* / , -           | < >         |

Extra Values are '<' for minimum value, such as 0 for minutes or 1 for months.
And '>' for maximum value, such as 23 for hours or 12 for months.

Supported special cases allow crontab lines to not use fields.
These are the supported aliases which are not available in SystemV mode:

|Case       |Meaning    |
|-----------|-----------|
|@reboot    |Every boot |
|@hourly    |0 * * * *  |
|@daily     |0 0 * * *  |
|@weekly    |0 0 * * 0  |
|@monthly   |0 0 1 * *  |
|@yearly    |0 0 1 1 *  |
|@annually  |0 0 1 1 *  |
|@midnight  |0 0 * * *  |

How to Use the Module
=====================

**Note:** Several users have reported their new crontabs not saving automatically. At this point you MUST use write() if you want your edits to be saved out. See below for full details on the use of the write function.

Getting access to a crontab can happen in five ways, three system methods that
will work only on Unix and require you to have the right permissions::

    from crontab import CronTab

    empty_cron    = CronTab()
    my_user_cron  = CronTab(user=True)
    users_cron    = CronTab(user='username')

And two ways from non-system sources that will work on Windows too::

    file_cron = CronTab(tabfile='filename.tab')
    mem_cron = CronTab(tab="""
      * * * * * command
    """)

Special per-command user flag for vixie cron format (new in 1.9)::

    system_cron = CronTab(tabfile='/etc/crontab', user=False)
    job = system_cron[0]
    job.user != None
    system_cron.new(command='new_command', user='root')

Creating a new job is as simple as::

    job  = cron.new(command='/usr/bin/echo')

And setting the job's time restrictions::

    job.minute.during(5,50).every(5)
    job.hour.every(4)
    job.day.on(4, 5, 6)

    job.dow.on('SUN')
    job.dow.on('SUN', 'FRI')
    job.month.during('APR', 'NOV')

Each time restriction will clear the previous restriction::

    job.hour.every(10) # Set to * */10 * * *
    job.hour.on(2)     # Set to * 2 * * *

Appending restrictions is explicit::

    job.hour.every(10)  # Set to * */10 * * *
    job.hour.also.on(2) # Set to * 2,*/10 * * *

Setting all time slices at once::

    job.setall(2, 10, '2-4', '*/2', None)
    job.setall('2 10 * * *')

Setting the slice to a python date object::

    job.setall(time(10, 2))
    job.setall(date(2000, 4, 2))
    job.setall(datetime(2000, 4, 2, 10, 2))

Run a jobs command. Running the job here will not effect it's
existing schedule with another crontab process::

    job_standard_output = job.run()

Creating a job with a comment::

    job = cron.new(command='/foo/bar', comment='SomeID')

Get the comment or command for a job::

    command = job.command
    comment = job.comment

Modify the comment or command on a job::

    job.set_command("new_script.sh")
    job.set_comment("New ID or comment here")

Disabled or Enable Job::

    job.enable()
    job.enable(False)
    False == job.is_enabled()

Validity Check::

    True == job.is_valid()

Use a special syntax::

    job.every_reboot()

Find an existing job by command::

    iter = cron.find_command('bar')

Find an existing job by comment::

    iter = cron.find_comment('ID or some text')

Find an existing job by schedule::

    iter = cron.find_time(2, 10, '2-4', '*/2', None)
    iter = cron.find_time("*/2 * * * *")

Clean a job of all rules::

    job.clear()

Iterate through all jobs, this includes disabled (commented out) cron jobs::

    for job in cron:
        print job

Iterate through all lines, this includes all comments and empty lines::

    for line in cron.lines:
        print line

Iterate through environment variables::

    for (name, value) in cron.env.items():
        print name
        print value

Create new or update enviroment variable::

    cron.env['SHELL'] = '/bin/bash'

Remove Items::

    cron.remove( job )
    cron.remove_all('echo')
    cron.remove_all(comment='foo')
    cron.remove_all(time='*/2')

Clear entire cron of all jobs::

    cron.remove_all()

Write CronTab back to system or filename::

    cron.write()

Write CronTab to new filename::

    cron.write( 'output.tab' )

Write to this user's crontab (unix only)::

    cron.write_to_user( user=True )

Write to some other user's crontab::

    cron.write_to_user( user='bob' )

Validate a cron time string::

    from crontab import CronSlices
    bool = CronSlices.is_valid('0/2 * * * *')

Proceeding Unit Confusion
=========================

It is sometimes logical to think that job.hour.every(2) will set all proceeding
units to '0' and thus result in "0 \*/2 * * \*". Instead you are controlling
only the hours units and the minute column is unaffected. The real result would
be "\* \*/2 * * \*" and maybe unexpected to those unfamiliar with crontabs.

There is a special 'every' method on a job to clear the job's existing schedule
and replace it with a simple single unit::

    job.every(4).hours()  == '0 */4 * * *'
    job.every().dom()     == '0 0 * * *'
    job.every().month()   == '0 0 0 * *'
    job.every(2).dows()   == '0 0 * * */2'

This is a convenience method only, it does normal things with the existing api.

Running the Scheduler
=====================

The module is able to run a cron tab as a daemon as long as the optional
croniter module is installed; each process will block and errors will
be logged (new in 2.0).

(note this functionality is new and not perfect, if you find bugs report them!)

Running the scheduler::

    tab = CronTab(tabfile='MyScripts.tab')
    for result in tab.run_scheduler():
        print "This was printed to stdout by the process."

Do not do this, it won't work because it returns generator function::

    tab.run_scheduler()

Timeout and cadence can be changed for testing or error management::

    for result in tab.run_scheduler(timeout=600):
        print "Will run jobs every 1 minutes for ten minutes from now()"

    for result in tab.run_scheduler(cadence=1, warp=True):
        print "Will run jobs every 1 second, counting each second as 1 minute"

Frequency Calculation
=====================

Every job's schedule has a frequency. We can attempt to calculate the number
of times a job would execute in a give amount of time. We have three simple
methods::

    job.setall("1,2 1,2 * * *")
    job.frequency_per_day() == 4

The per year frequency method will tell you how many days a year the
job would execute::

    job.setall("* * 1,2 1,2 *")
    job.frequency_per_year(year=2010) == 4

These are combined to give the number of times a job will execute in any year::

    job.setall("1,2 1,2 1,2 1,2 *")
    job.frequency(year=2010) == 16

Frequency can be quickly checked using python built-in operators::

    job < "*/2 * * * *"
    job > job2
    job.slices == "*/5"

Log Functionality
=================

The log functionality will read a cron log backwards to find you the last run
instances of your crontab and cron jobs.

The crontab will limit the returned entries to the user the crontab is for::

    cron = CronTab(user='root')

    for d in cron.log:
        print d['pid'] + " - " + d['date']

Each job can return a log iterator too, these are filtered so you can see when
the last execution was::

    for d in cron.find_command('echo')[0].log:
        print d['pid'] + " - " + d['date']

All System CronTabs Functionality
=================================

The crontabs (note the plural) module can attempt to find all crontabs on the
system. This works well for Linux systems with known locations for cron files
and user spolls. It will even extract anacron jobs so you can get a picture
of all the jobs running on your system::

    from crontabs import CronTabs
    
    for cron in CronTabs():
        print repr(cron)

All jobs can be brought together to run various searches, all jobs are added
to a CronTab object which can be used as documented above::

   jobs = CronTabs().all.find_command('foo')

Schedule Functionality
======================

If you have the croniter python module installed, you will have access to a
schedule on each job. For example if you want to know when a job will next run::

    schedule = job.schedule(date_from=datetime.now())

This creates a schedule croniter based on the job from the time specified. The
default date_from is the current date/time if not specified. Next we can get
the datetime of the next job::

    datetime = schedule.get_next()

Or the previous::

    datetime = schedule.get_prev()

The get methods work in the same way as the default croniter, except that they
will return datetime objects by default instead of floats. If you want the
original functionality, pass float into the method when calling::

    datetime = schedule.get_current(float)

If you don't have the croniter module installed, you'll get an ImportError when
you first try using the schedule function on your cron job object.

Descriptor Functionality
========================

If you have the cron-descriptor module installed, you will be able to ask for a
translated string which describes the frequency of the job in the current
locale language. This should be mostly human readable.


    print(job.description(use_24hour_time_format=True))

See cron-descriptor for details of the supported languages and options.

Extra Support
=============

 - Support for vixie cron with username addition with user flag
 - Support for SunOS, AIX & HP with compatibility 'SystemV' mode.
 - Python 3.4 and Python 2.7/2.6 tested.
 - Windows support works for non-system crontabs only.
   ( see mem_cron and file_cron examples above for usage )
