<?php header('Content-Type: application/json') ?>

<?php $comments_out = array() ?>

<?php foreach ($comments as $row): ?>
  <?php $comment_out = array_merge((array)$row, array(
    'created' => date('Y-m-d h:i:s', $row->created),
  )) ?>

  <?php $comments_out[] = $comment_out ?>
<?php endforeach ?>

<?php echo json_encode(array(
  'information' => $information,
  'comments'    => $comments_out,
  'pagination'  => $pagination,
)) ?>