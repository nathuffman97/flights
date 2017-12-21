<?php
  function dbconnect() {
    $PDO_CONN = 'pgsql:host=flights.cd3htbuk9dcu.us-east-2.rds.amazonaws.com;port=5432;dbname=flights';
    $PDO_USER = 'root';
    $PDO_PASS = 'OUintaPATHOUGhBRAirc';
    $dbh = new PDO($PDO_CONN, $PDO_USER, $PDO_PASS);
    $dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $dbh->setAttribute(PDO::ATTR_EMULATE_PREPARES, false); 
    return $dbh;
  }
?>
