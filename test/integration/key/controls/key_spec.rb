control 'key-01' do
  impact 1.0
  title 'Key create'
  describe file('/var/www/miq/vmdb/certs/v2_key') do
    it { should exist }
  end
end
