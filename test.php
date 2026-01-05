<?php
// === 必须最先定义所有常量 ===
define('UC_CONNECT', 'default');
define('UC_STANDALONE', 0);
//define('UC_DBHOST', '127.0.0.1');
//define('UC_DBUSER', 'root');
//define('UC_DBPW', 'J9Yq9aLpPsFswuz4');
//define('UC_DBNAME', 'ultrax');
//define('UC_DBCHARSET', 'utf8mb4');
//define('UC_DBTABLEPRE', '`ultrax`.pre_ucenter_');
//define('UC_DBCONNECT', '0');
define('UC_AVTURL', '');
define('UC_AVTPATH', '');
define('UC_KEY', 'Z1mfdafsfjhofdiuhaoufhefonaf6q0s2Be4embDeN7j8Ed84A6geCcB1Yb0c');
define('UC_API', 'http://192.168.10.139:8080/uc_server');
define('UC_CHARSET', 'utf-8');
define('UC_IP', '');
define('UC_APPID', '2');
define('UC_PPP', '20');

// ===========================

// 错误显示
error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "1. 准备加载 uc_client...\n";

// 注册 shutdown 函数（用于捕获后续可能的 fatal error）
register_shutdown_function(function() {
    $error = error_get_last();
    if ($error && in_array($error['type'], [E_ERROR, E_PARSE, E_CORE_ERROR, E_COMPILE_ERROR])) {
        echo "\n? 致命错误: {$error['message']} in {$error['file']}:{$error['line']}\n";
    }
});

// 加载 uc_client
include __DIR__ . '/uc_client/client.php';

echo "2. uc_client 加载成功！\n";

if (function_exists('uc_user_login')) {
    echo "3. uc_user_login 函数可用。\n";

    // 可选：测试登录
    $result = @uc_user_login('admin', 'admin', 0, 0, '', '');
    echo "4. 登录测试结果: " . json_encode($result, JSON_UNESCAPED_UNICODE) . "\n";
} else {
    echo "3. ? 函数不可用！\n";
}
