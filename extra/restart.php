<?
// Restarts FCGI. modify as required.
	if(filter_var($_GET['p'], FILTER_SANITIZE_STRING) == "a_password"){
		$cmd = "ps aux | grep python; killall /usr/bin/python; "."python /home/cs215/project/manage.py runfcgi method=prefork host=127.0.0.1 port=9090";
		echo exec($cmd);
		echo "\ndone\n";
	}
?>
