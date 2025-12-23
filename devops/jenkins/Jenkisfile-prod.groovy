@Library('jenkins-sharedlib')

def repo_sh = "https://github.com/odoopartners/tailoringconsulting-jayala.git"
def submodule_branch = '17.0'

buildPipelineOdooSH(repo_sh: "${repo_sh}", submodule_branch: "${submodule_branch}")
