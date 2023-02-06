require_once 'libs/Requests/src/Autoload.php';
WpOrg\Requests\Autoload::register();

$headers = array('Accept' => 'application/json');
$options = array('auth' => array('user', 'pass'));
$request = WpOrg\Requests\Requests::get('https://api.github.com/gists', $headers, $options);

var_dump($request->status_code);
// int(200)

var_dump($request->headers['content-type']);
// string(31) "application/json; charset=utf-8"

var_dump($request->body);
// string(26891) "[...]"
