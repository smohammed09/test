/*** BEGIN META {
 "name" : "Discard old builds",
 "comment" : "Changes the config of the builds to discard old builds (only if no log rotation is configured).",
 "parameters" : [ 'dryRun', 'daysToKeep', 'numToKeep', 'artifactDaysToKeep', 'artifactNumToKeep'],
 "core": "2.46.2",
 "authors" : [
 { name : "Mestachs" }, { name : "Dominik Bartholdi" }, { name: "Denys Digtiar" }
 ]
 } END META**/

// NOTES:
// dryRun: to only list the jobs which would be changed
// daysToKeep:  If not -1, history is only kept up to this days.
// numToKeep: If not -1, only this number of build logs are kept.
// artifactDaysToKeep: If not -1 nor null, artifacts are only kept up to this days.
// artifactNumToKeep: If not -1 nor null, only this number of builds have their artifacts kept.

dryRun=false
daysToKeep=-1
artifactDaysToKeep=-1
numToKeep=7
artifactNumToKeep=-1

import jenkins.model.Jenkins
import hudson.model.Job
import hudson.tasks.LogRotator

Jenkins.instance.allItems(Job).each { job ->
    if(!job.isBuildable()) return
    if(!job.supportsLogRotator()) return
    if(job.getBuildDiscarder() != null && (job.getBuildDiscarder().getNumToKeep() != -1 || job.getBuildDiscarder().getDaysToKeep() != -1)) return

    if (!"true".equals(dryRun)) {
        // adding a property implicitly saves so no explicit one
        job.setBuildDiscarder(new LogRotator ( daysToKeep, numToKeep, artifactDaysToKeep, artifactNumToKeep))
        println "${job.displayName} is updated"
    }
}
return;
