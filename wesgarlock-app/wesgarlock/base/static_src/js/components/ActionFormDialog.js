/* global csrf_input */
import React from 'react'
import PropTypes from 'prop-types'
import { Dialog, DialogContent, Box, withStyles } from '@material-ui/core'
import DialogTitleWithCloseIcon from './DialogTitleWithCloseIcon'
import parse from 'html-react-parser'

const styles = theme => ({
  dialogPaper: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    paddingBottom: theme.spacing(3),
    maxWidth: 420
  },
  actions: {
    marginTop: theme.spacing(2)
  },
  dialogPaperScrollPaper: {
    maxHeight: 'none'
  },
  dialogContent: {
    paddingTop: 0,
    paddingBottom: 0
  }
})

/**
 * A Wrapper around the Dialog component to create centered
 * Login, Register or other Dialogs.
 */
function ActionFormDialog (props) {
  const {
    classes,
    open,
    onClose,
    loading,
    headline,
    onFormSubmit,
    content,
    actions,
    hideBackdrop,
    actionUrl,
    method
  } = props
  console.log(actionUrl)

  return (
    <Dialog
      open={open}
      onClose={onClose}
      disableBackdropClick={loading}
      disableEscapeKeyDown={loading}
      classes={{
        paper: classes.dialogPaper,
        paperScrollPaper: classes.dialogPaperScrollPaper
      }}
      hideBackdrop={hideBackdrop || false}
    >
      <DialogTitleWithCloseIcon
        title={headline}
        onClose={onClose}
        disabled={loading}
      />
      <DialogContent className={classes.dialogContent}>
        <form method={method} action={actionUrl} onSubmit={onFormSubmit}>
        {parse(csrf_input)}
          <div>{content}</div>
          <Box width="100%" className={classes.actions}>
            {actions}
          </Box>
        </form>
      </DialogContent>
    </Dialog>
  )
}

ActionFormDialog.propTypes = {
  classes: PropTypes.object.isRequired,
  open: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  headline: PropTypes.string.isRequired,
  loading: PropTypes.bool.isRequired,
  onFormSubmit: PropTypes.func.isRequired,
  content: PropTypes.element.isRequired,
  actions: PropTypes.element.isRequired,
  hideBackdrop: PropTypes.bool.isRequired,
  actionUrl: PropTypes.string.isRequired,
  method: PropTypes.string.isRequired
}

export default withStyles(styles, { withTheme: true })(ActionFormDialog)
