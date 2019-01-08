package My::ExamLib;
use strict;
use warnings;

use Exporter qw(import);
our @EXPORT_OK = qw(ins_gpl timestamp_expired compute_mac dienice random_int);

#-----------------------------------
sub ins_gpl
{
print qq+<!--\n+;
print qq!SimEx Radio Release \n!;
print qq!SimEx Radio was created originally for YO6KXP radio amateur club located in\n!; 
print qq!Sacele, ROMANIA (YO) then released to the whole radio amateur community.\n!;
print qq!\n!;
print qq!Prezentul simulator de examen impreuna cu formatul bazelor de intrebari, rezolvarile problemelor, manual de utilizare,\n!; 
print qq!instalare, SRS, cod sursa si utilitarele aferente constituie un pachet software gratuit care poate fi distribuit/modificat in \n!;
print qq!termenii licentei libere GNU GPL, asa cum este ea publicata de Free Software Foundation in versiunea 2 sau intr-o versiune \n!;
print qq!ulterioara. Programul, intrebarile si raspunsurile sunt distribuite gratuit, in speranta ca vor fi folositoare, dar fara nicio \n!;
print qq!garantie, sau garantie implicita, vezi textul licentei GNU GPL pentru mai multe detalii. Utilizatorul programului, \n!;
print qq!manualelor, codului sursa si utilitarelor are toate drepturile descrise in licenta publica GPL.\n!;
print qq!In distributia de pe https://github.com/6oskarwN/Sim_exam_yo trebuie sa gasiti o copie a licentei GNU GPL, de asemenea \n!;
print qq!si versiunea in limba romana, iar daca nu, ea poate fi descarcata gratuit de pe pagina http://www.fsf.org/\n!;
print qq!Textul intrebarilor oficiale publicate de ANCOM face exceptie de la cele de mai sus, nefacand obiectul licentierii GNU GPL, \n!;
print qq!copyrightul fiind al statului roman, dar fiind folosibil in virtutea legii 544/2001 privind liberul acces la informatiile \n!;
print qq!de interes public precum al legii 109/2007 privind reutilizarea informatiilor din institutiile publice.\n!;
print qq!\n!;
print qq!YO6OWN Francisc TOTH\n!;
print qq!\n!;
print qq!This program together with question database formatting, solutions to problems, manuals, documentation, sourcecode \n!;
print qq!and utilities is a  free software; you can redistribute it and/or modify it under the terms of the GNU General Public License \n!;
print qq!as published by the Free Software Foundation; either version 2 of the License, or any later version. This program is distributed \n!;
print qq!in the hope that it will be useful, but WITHOUT ANY WARRANTY or without any implied warranty. See the GNU General Public \n!;
print qq!License for more details. You should have received a copy of the GNU General Public License along with this software distribution; \n!;
print qq!if not, you can download it for free at http://www.fsf.org/ \n!;
print qq!Questions marked with ANCOM makes an exception of above-written, as ANCOM is a romanian public authority(similar to FCC \n!;
print qq!in USA) so any use of the official questions, other than in Read-Only way, is prohibited. \n!;
print qq!\n!;
print qq!YO6OWN Francisc TOTH\n!;
print qq!\n!;
print qq!Made in Romania\n!;
print qq+-->\n+;

}

#--------------------------------------
#primeste timestamp de forma sec_min_hour_day_month_year UTC
#out: seconds since expired MAX 99999, 0 = not expired.
#UTC time and epoch are used

sub timestamp_expired
{
use Time::Local;

my($x_sec,$x_min,$x_hour,$x_day,$x_month,$x_year)=@_;

my $timediff;
my $actualTime = time(); #epoch since UTC0000
my $dateTime= timegm($x_sec,$x_min,$x_hour,$x_day,$x_month,$x_year);
$timediff=$actualTime-$dateTime;

return($timediff);  #here is the general return

} #.end sub timestamp

#--------------------------------------
sub compute_mac {

use Digest::HMAC_SHA1 qw(hmac_sha1_hex);
  my ($message) = @_;
  my $secret = '80b3581f9e43242f96a6309e5432ce8b'; #development secret
  hmac_sha1_hex($secret,$message);
} #end of compute_mac

#-------------------------------------
# treat the "or die" and all error cases
#how to use it
#$error_code is a string, you see it, this is the text selector
#$counter: if it is 0, error is not logged. If 1..5 = threat factor
#reference is the reference to string that is passed to be logged.
#ERR19 and ERR20 have special handling regarding the browser error display

sub dienice
{
my ($error_code,$counter,$err_reference)=@_; #in vers. urmatoare counter e modificat in referinta la array/string

my $timestring=gmtime(time);

my($package,$filename,$line)=caller;

#textul pentru public
my %pub_errors= (
              "ERR00" => "error: unknown/unspecified",
              "authERR01" => "primire de  date corupte.",
              "gen0ERR01" => "Server congestionat, incearca in cateva momente",
              "genERR01" => "actiune ilegala, inregistrata in log",

              "authERR02" => "primire de date corupte",
              "gen0ERR02" => "Server congestionat, incearca in cateva momente",
              "genERR02" => "timpul alocat formularului a expirat",

              "authERR03" => "Credentiale incorecte.<br><br>ATENTIE: Daca ai avut un cont mai demult si nu te-ai mai logat de peste 14 zile, contul tau s-a sters automat", #CUSTOM nr zile
              "genERR03" => "server congestionat",

              "authERR04" => "Autentificarea blocata pentru o perioada de 5 minute pentru incercari repetate cu credentiale incorecte. Incercati din nou dupa expirarea periodei de penalizare.",
              "genERR04" => "server congestionat",

              "authERR05" => "Autentificare imposibila cu credentialele furnizate",
              "genERR05" => "server congestionat",

              "authERR06" => "Autentificarea blocata pentru o perioada de 5 minute pentru incercari repetate cu credentiale incorecte. Incercati din nou dupa expirarea periodei de penalizare.",
              "genERR06" => "server congestionat",

              "authERR07" => "examyo system error, logged for admin",
              "genERR07" => "server congestionat",

              "authERR08" => "congestie server, incearca in cateva momente",
              "genERR08" => "server congestionat",

              "authERR09" => "congestie server, incearca in cateva momente",
              "genERR09" => "Aceasta cerere nu este recunoscuta de sistem, cererea a fost logata",

              "authERR10" => "congestie server, incearca in cateva momente",
              "genERR10" => "actiune ilegala, inregistrata in log",

              "genERR11" => "server congestionat",
              "genERR12" => "actiune ilegala, inregistrata in log",
              "genERR13" => "server congestionat",
              "genERR14" => "server congestionat",
              "genERR15" => "formularul a fost deja folosit odata",
              "genERR16" => "congestie server",
              "genERR17" => "actiune ilegala, inregistrata in log",
              "genERR18" => "actiune ilegala, inregistrata in log",

              "ERR19" => "error not displayed",
              "ERR20" => "silent discard"	
                );
#textul de turnat in logfile, interne
my %int_errors= (
              "ERR00" => "unknown/unspecified",
              "authERR01" => "not exactly 2 pairs received",            #test ok
              "gen0ERR01" => "server cannot open sim_transaction file",    #test
              "genERR01" => "transaction sha1 authenticity failed",   #untested

              "authERR02" => "2 pairs but not login and passwd",        #test ok
              "genERR02" => "transaction timestamp expired, normally not logged",            

              "gen0ERR02" => "server cannot open db_human file",           #test
              "authERR03" => "cont inexistent sau expirat",             #test ok
              "genERR03" => "fail open sim_transaction file",           #tested

              "authERR04" => "normally not logged",
              "genERR04" => "fail close sim_transaction file",

              "authERR05" => "normally not logged, we should just count them somewhere",
              "genERR05" => "fail open sim_users file",                 #tested

              "authERR06" => "3xfailed authentication for existing user",
              "genERR06" => "fail open existing user's hlrfile",        #tested

              "authERR07" => "examyo system error, should never occur, weird hlr_class:",
              "genERR07" => "fail create new hlrfile",                  #tested

              "authERR08" => "cannot open file",
              "genERR08" => "fail close sim_users",

              "authERR09" => "cannot close file",
              "genERR09" => "good and unexpired received trid but not in tridfile. Under attack?",

              "authERR10" => "cannot open hlr file",
              "genERR10" => "from wrong pagecode invoked generation of exam",

              "genERR11" => "fail close transaction file",
              "genERR12" => "wrong clearance level to request this exam",
              "genERR13" => "fail open user's hlrfile",
              "genERR14" => "fail open one of db_ file",
              "genERR15" => "transaction id already used, normally not logged",
              "genERR16" => "fail close one of db_file",
              "genERR17" => "received trid is undef",
              "genERR18" => "received trid is destruct",

              "ERR19" => "silent logging(if $counter>0), not displayed",
	      "ERR20" => "silent discard,(logged only if $counter>0)"
                );


#if commanded, write errorcode in cheat_file
if($counter > 0)
{
# write errorcode in cheat_file

# count the number of lines in the db_tt by counting the '\n'
# open read-only the db_tt
my $CountLines = 0;
my $filebuffer;
#TBD - flock to be analysed if needed or not on the read-only count
           open(DBFILE,"< db_tt") or die "Can't open db_tt";
           while (sysread DBFILE, $filebuffer, 4096) {
               $CountLines += ($filebuffer =~ tr/\n//);
           }
           close DBFILE;

#CUSTOM limit db_tt writing to max number of lines (4 lines per record) 
if($CountLines < 200) #CUSTOM max number of db_tt lines (200/4=50 records)
{
#ACTION: append cheat symptoms in cheat file
open(cheatFILE,"+< db_tt"); #open logfile for appending;
#flock(cheatFILE,2);		#LOCK_EX the file from other CGI instances
seek(cheatFILE,0,2);		#go to the end
#CUSTOM
printf cheatFILE qq!cheat logger\n$counter\n!; #de la 1 la 5, threat factor
printf cheatFILE "\<br\>reported by: %s\<br\>  %s: %s \<br\> UTC Time: %s\<br\>  Logged:%s\n\n",$filename,$error_code,$int_errors{$error_code},$timestring,$$err_reference; #write error info in logfile
close(cheatFILE);
} #.end max number of lines
} #.end $counter>0

if($error_code eq 'ERR20') #must be silently discarded with Status 204 which forces browser stay in same state
{
print qq!Status: 204 No Content\n\n!;
print qq!Content-type: text/html\n\n!;
}
else
{
unless($error_code eq 'ERR19'){ #ERR19 is silent logging, no display, no exit()
print qq!Content-type: text/html\n\n!;
print qq?<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n?; 
print qq!<html>\n!;
print qq!<head>\n<title>examen radioamator</title>\n</head>\n!;
print qq!<body bgcolor="#228b22" text="#7fffd4" link="white" alink="white" vlink="white">\n!;
ins_gpl(); #this must exist
print qq!v 3.2.7\n!; #version print for easy upload check
print qq!<br>\n!;
print qq!<h1 align="center">$pub_errors{$error_code}</h1>\n!;
print qq!<form method="link" action="http://localhost/index.html">\n!;
print qq!<center><INPUT TYPE="submit" value="OK"></center>\n!;
print qq!</form>\n!; 
print qq!</body>\n</html>\n!;
                              }
}

exit();

} #end sub

#----100%------subrutina generare random number
# intoarce numar intre 0 si $max-1
sub random_int($)
	{
	
	my ($max)=@_;

       return int(rand($max));
	}

#----- don't know what for, but it should return something probably
1;
