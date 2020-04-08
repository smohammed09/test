library 'jenkins-shared-pipeline-library'
import jenkins.model.Jenkins

node('aws-ec2') {
    def body = "<h1>This  page updated by</h1><a href=\\\"Sandbox Jenkinstein - Testing\\\">Jenkins Job</a>"
    body += '<table><colgroup><col/><col/><col/></colgroup><tbody><tr><th>DisplayName (Click on the name for more info)</th><th>ShortName</th><th>CurrentVersion</th><th>LatestVersion</th></tr>'

    def total_installed_plugins = 0
    def outdated_plugins = 0
    Jenkins.instance.pluginManager.plugins.each{
        plugin ->
        total_installed_plugins += 1
        def newPlugin = plugin.getUpdateInfo()
        def new_version = "UpToDate"
        if (newPlugin != null) {
            new_version = newPlugin.version
            outdated_plugins += 1
        }
        
        body += ("<tr><td><a href=\\\"${plugin.getUrl()}\\\">${plugin.getDisplayName()}</a></td><td>${plugin.getShortName()}</td><td>${plugin.getVersion()}</td><td>${new_version}</td></tr>")
    }
    
    def  latestLTSVersionAvailable = getJenkinsLatestLTSVersion()
    
    def upToDate_plugins = total_installed_plugins - outdated_plugins

    body += '</tbody></table>'
    body += "<b><br/>Total installed plugins = $total_installed_plugins &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Total updated plugins = $upToDate_plugins &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Total out of date plugins = $outdated_plugins</b>"


    // pageId: 58143262 is the Test page
    confluence.updatePage('58143262', 'Test Metrics Dashboard', body)

    String currentCoreVersion = Jenkins.instance.getVersion()

    /* Send data to splunk
    */
    def payload = [
        "job_name": env.JOB_NAME,
        "Total_plugins": total_installed_plugins,
        "UpToDate_plugins": upToDate_plugins,
        "Outdated_plugins": outdated_plugins,
        "LatestLTSVersionAvailable": latestLTSVersionAvailable,
        "CurrentCoreVersion": currentCoreVersion,
    ]
    splunkins.send(payload)
}