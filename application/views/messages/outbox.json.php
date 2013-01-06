<?php

$messages_json = array();

foreach($messages->result() as $row) {
    $usernames = explode(',', $row->usernames);

    $messages_json[] = array(
        'created'    => date(DateTime::ISO8601, strtotime($row->created)),
        'message_id' => (int)$row->message_id,
        'subject'    => $row->subject,
        'usernames'  => $usernames,
    );
}

?>

<?php echo json_encode($messages_json) ?>