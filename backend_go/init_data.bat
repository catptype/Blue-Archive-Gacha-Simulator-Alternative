@echo off
set CGO_ENABLED=1
go run commands/seeder/seeder.go
pause