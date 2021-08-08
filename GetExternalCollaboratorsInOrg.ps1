<#This script will give outside collaborators information  in organization in CSV file #>

#----------------------------Variables Declaration------------------------------------------------------------------------------------------------------------------------------------------
$org = "mygithuborg"  #Change GitHub Organization Name here
$GitHubTokenNo = "Bearer <Enter Your PAT Token here>" #Enter your GitHub PAT here for authorisation..for example here which is starting with  816
$csvfile = "c:\temp\GitHubOutsideCollaborators.csv" #Your CSV file path.If file not present initially, the script will automatically create the file at the path
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#----------------------Authentication & Custom Object Function Creation--------------------------------------------------------------------------------------------------------------------

$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$headers.Add("Authorization", $GitHubTokenNo)
$headers.Add("Content-Type","application/json")


Clear-Content -Path $csvfile -ErrorAction SilentlyContinue

function WriteTo-File($login,$reponame,$htmlurl,$siteadmin,$permissions,$type)
{
    [PSCustomObject]@{
    UserLoginName = $login
    Reponame = $rname
    RepoUrl = $repourl
    UserHtmlUrl = $htmlurl
    SiteAdmin = $site_admin
    Permissions = $permissions
    Type = $type

    }  | Export-Csv $csvfile -Append -NoTypeInformation
}

#------------------------Working ON API's-----------------------------------------------------------------------------------------------------------------------------------------------------

$response = Invoke-RestMethod "https://api.github.com/orgs/$org/repos" -Method 'GET' -Headers $headers -Body $body 
foreach($r in $response)
{
$rname = $r.name
$repohtmlurl = $r.html_url
$outsidecollaborators = $null
$outsidecollaborators = Invoke-RestMethod "https://api.github.com/repos/$org/$rname/collaborators?affiliation=outside" -Method 'GET' -Headers $headers -Body $body 
if($outsidecollaborators -ne $null)
{
foreach($oc in $outsidecollaborators)
{
$login = $oc.login
$reponame = $rname
$repourl = $repohtmlurl
$htmlurl = $oc.html_url
$site_admin = $oc.site_admin
$permissions = $oc.permissions
$type = $oc.type
#WriteTo-File($login,$reponame,$htmlurl,$siteadmin,$permissions,$type) 
WriteTo-File -login $login -reponame $rname -htmlurl $htmlurl -siteadmin $site_admin -permissions $permissions -type $type  #Write to Function
Write-Output "$login,$reponame,$htmlurl,$siteadmin,$permissions,$type" #Write Output on Console
}
}
}
