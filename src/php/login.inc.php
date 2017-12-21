<?php

session_start();

if (isset($_POST['submit'])) {

	include 'pdo-mine.php';
	$dbh = dbconnect();


	$email = mysqli_real_escape_string($dbh,$_POST['email']);
	$pwd = mysqli_real_escape_string($dbh,$_POST['pwd']);

	//Error handlers
	// empty input check
	if (empty($email)|| empty($pwd)){
		header("Location: index.php?login=empty");
		exit();

	} else{
		$sql = "SELECT * FROM people WHERE Email = '$email'";
		$result = mysqli_query($dbh,$sql);
		$resultCheck = mysqli_num_rows($result);
		if($resultCheck < 1){
			header("Location: index.php?login=error");
			exit();
		} else {
			if($row = mysqli_fetch_assoc($result)){
				//De-hashing password
				$hashedPwdCheck = password_verify($pwd, $row['Pwd']);
				if ($hashedPwdCheck == false){
					header("Location: index.php?login=error");
					exit();
				} elseif ($hashedPwdCheck == true) {
					// log in the user
					$_SESSION['email']=$row['Email'];
					$_SESSION['username']=$row['Username'];
					$_SESSION['u_id']=$row['id'];
					header("Location: index.php?login=success");
					exit();
				}
			}
		}
	}
} else{
	header("Location: index.php?login=error");
	exit();
}