#©2013 Drew Crawford Apps.  All Rights Reserved.
#See LICENSE file for details.

__version__="0.2.0-dev"

#This is the port that clients use to connect to the caffeine router
client_port = 55555

#This is the port that moves data from the router to the server worker process
internal_url = "ipc://caffeine_router"


#This is a well-known key that should ONLY BE USED FOR TESTING.
well_known_public_key = b'+mJ$T/MtfudE4ayALn7.ds.^A4@DLgFwCgLU)REV'

#This is a well-known key that should ONLY BE USED FOR TESTING.
well_known_private_key = b'sT6er}nZM.%bttBGHB+F*8mr^JJ}r#V<)du8KXup'


number_of_worker_processes = 4

