semaphore mutex = 1, block = 0;				/* share variables: semaphores, */
int active = 0, waiting = 0; 				/* counters, and */	
boolean must_wait = false;					/* state information */
semWait(mutex) ;							/* Enter the mutual exclusion */
if(must_wait) {                             /* If there are (or were) 3, then */
    ++waiting;                              /* we must wait, but we must leave */
    semSignal(mutex) ;                      /* the mutual exclusion first */
    semWait(block) ;                        /* Wait for all current users to depart */
    --waiting;                              
}

++active;                                   /* Update active count, and remember */
must_wait = active == 3;                    /* if the count reached 3 */
if (waiting > 0 && !must_wait ){
    semSignal(block);                       /* If there are waiting processes, */
}
else semSignal(mutex) ;                    


/* critical section */

semWait(mutex);                             /* Enter mutual exclusion */
--active;                                   /* and update the active count */
if(active == 0) {                           /* Last one to leave? */
    must_wait = false;                      /* All active processes have left */
}
if (waiting > 0 && !must_wait) {            
    semSignal(block);                       
}
else semSignal (mutex) ;                         /* Leave the mutual exclusion */