<?php

$message_json = array(
    'sender_id'  => (int)$message->sender_id,
    'to_id'      => (int)$message->to_id,
    'content'    => $message->content,
    'created'    => date(DateTime::ISO8601, strtotime($message->created)),
    'is_read'    => '1' === $message->read,
    'message_id' => (int)$message->message_id,
    'subject'    => $message->subject,
    'username'   => $message->username,
);

?>

<?php echo json_encode($message_json) ?>