control 'database-01' do
  impact 1.0
  title 'Database present'
  describe file('/var/www/miq/vmdb/config/database.yml') do
    it { should exist }
  end
  describe bash('cd /var/www/miq/vmdb; bin/rake db:version') do
    its('stdout') { should match /Current version/ }
    its('exit_status') { should eq 0 }
  end
  describe processes('postgres') do
    its('list.length') { should >= 0 }
  end
end

control 'database-02' do
  impact 1.0
  title 'Database absent'
  describe processes('postgres') do
    its('list.length') { should eq 0 }
  end
  describe service('evmserverd') do
    it { should_not be_running }
  end
  describe file('/var/www/miq/vmdb/config/database.yml') do
    it { should_not exist }
  end
  describe file('/var/opt/rh/rh-postgresql95/lib/pgsql/data/') do
    its('content') { should match nil }
  end
end

control 'database-03' do
  impact 1.0
  title 'Database backup'
  describe file('/tmp/backup') do
    it { should exist }
  end
end

control 'database-04' do
  impact 1.0
  title 'Database reset'
  describe http('https://localhost/api/users',
                auth: {user: 'admin', pass: 'smartvm'},
                method: 'GET', ssl_verify: false,
                enable_remote_worker: true) do
    its('body') { should match /"count":1/ }
    its('status') { should eq 200 }

  end
end

control 'database-05' do
  impact 1.0
  title 'Database restore'
  describe http('https://localhost/api/users/1000000000002',
                auth: {user: 'admin', pass: 'smartvm'},
                method: 'GET', ssl_verify: false,
                enable_remote_worker: true) do
    its('status') { should eq 200 }

  end
end
