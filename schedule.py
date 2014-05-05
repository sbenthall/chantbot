'''
Deprecated scheduling functions
'''

def compute_start():
    start_time = dtime(*time.strptime(config.get('Schedule',
                                                 'starttime'),"%H:%M")[3:5])
    now = datetime.now()

    if now.time() < start_time:
        start_day = now
    else:
        tomorrow = tomorrow = datetime.fromordinal(now.toordinal() + 1)
        start_day = tomorrow

    start = datetime.combine(start_day,start_time)
    return start

def do_chant(chant):

    interval = duration / (len(chant.bursts) - 1)
    rest = interval - chant.lpb * beat

    logger.debug("Interval: %d. Rest: %d." % (interval,rest))

    for burst in chant.bursts:
        for line in burst:
            t.statuses.update(status=line)
            logger.debug(line)
            time.sleep(beat)

        logger.debug("(rest)")
        time.sleep(rest)


'''
    chants = itertools.cycle(chants)

    # burn in to appropriate starting chant
    for i in range(chantburn):
        logger.debug("Burning in for %d." % chantburn)
        chants.next()

        index = chantburn

        for chant in chants:
            logger.debug("Computing start time")
            start = compute_start()
            wait = start - datetime.now()
            logger.debug("Waiting for %s for next chant." % wait)
            time.sleep(wait.total_seconds())
            logger.debug("Beginning chant index %d" % index)
            do_chant(chant)
'''
