pipx run cibuildwheel --platform linux --archs x86_64
#start-job {pipx run cibuildwheel --platform linux --archs aarch64}
#start-job {pipx run cibuildwheel --platform windows --archs amd64}
#
## Wait for it all to complete
#While (Get-Job -State "Running")
#{
#    Start-Sleep 10
#}
#
#python -m twine upload wheelhouse/*