<?php

if (isset($_POST['submit'])) {
	
	include_once 'pdo-mine.php';
	$dbh = dbconnect();

	$user = mysqli_real_escape_string($dbh,$_POST['username']);
	$email = mysqli_real_escape_string($dbh,$_POST['email']);
	$pwd = mysqli_real_escape_string($dbh,$_POST['pwd']);

	//Error handlers
	//check for empty fields
	if (empty($user)||empty($email)||empty($pwd)){
		header("Location: signup.php?signup=empty");
		exit();
	} else {
		//Check input validity
		if(!preq_match("/^[a-zA-Z*$/]",$user)){
			header("Location: signup.php?signup=invalid");
			exit();
		} else{
			//check email validity
			if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
				header("Location: signup.php?signup=email");
				exit();
			} else {
				$sql = "SELECT * FROM people WHERE Email='$email'";
				$result = mysqli_query($dbh,$sql);
				$resultCheck = mysqli_num_rows($result);

				if($resultCheck > 0){
					header("Location: signup.php?signup=existing_account");
					exit();
				} else {
					//Hashing the password
					$hashedPwd = password_hash($pwd, PASSWORD_DEFAULT);
					//insert user into database
					$sql = "INSERT INTO people (Username, Email, Pwd) VALUES ('$user', '$email', '$hashedPwd');";
					mysqli_query($dbh, $sql);

					header("Location: signup.php?signup=success");
					exit();
				}
			}
		}
	}


} else{
	header("Location: signup.php");
	exit();
}