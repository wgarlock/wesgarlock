/* global context */

import React, { useState, useCallback } from 'react'
import PropTypes from 'prop-types'
import {
  TextField,
  Dialog,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  withStyles
} from '@material-ui/core'
import ButtonCircularProgress from '../../components/ButtonCircularProgress'
import { request } from '../../../../../base/static_src/js/api/request'

const styles = (theme) => ({
  dialogContent: {
    paddingTop: theme.spacing(2)
  },
  dialogActions: {
    paddingTop: theme.spacing(2),
    paddingBottom: theme.spacing(2),
    paddingRight: theme.spacing(2)
  }
})

function ChangePassword (props) {
  const { onClose, classes, setLoginStatus } = props
  const [isLoading, setIsLoading] = useState(false)
  const [response, setResponse] = useState('')

  const sendPasswordEmail = useCallback((e) => {
    setIsLoading(true)
    request({ url: context.front_urls.front_password_reset, method: 'POST', body: { email: e.target.elements.email.value } }).then(data => {
      const response = JSON.parse(data)
      setResponse(response.result)
      setIsLoading(false)
    }).catch(err => {
      console.log(err)
      setIsLoading(false)
    })
  }, [setIsLoading, setLoginStatus, onClose])

  return (
    <Dialog
      open
      hideBackdrop
      onClose={onClose}
      disableBackdropClick={isLoading}
      disableEscapeKeyDown={isLoading}
      maxWidth="xs"
      id="forgot-password-dialog"
    >
      <form
        onSubmit={(e) => {
          e.preventDefault()
          sendPasswordEmail(e)
        }}
      >

        <DialogContent className={classes.dialogContent}>
          <Typography paragraph>
            Enter your email address below and we will send you instructions on
            how to reset your password.
          </Typography>
          <Typography paragraph >
            {response}
          </Typography>
          <TextField
            variant="outlined"
            margin="dense"
            required
            fullWidth
            label="Email Address"
            autoFocus
            type="email"
            name="email"
            autoComplete="off"
          />
        </DialogContent>
        <DialogActions className={classes.dialogActions}>
          <Button onClick={onClose} disabled={isLoading}>
            Cancel
          </Button>
          <Button
            type="submit"
            variant="contained"
            color="secondary"
            disabled={isLoading}
          >
            Reset password
            {isLoading && <ButtonCircularProgress />}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  )
}

ChangePassword.propTypes = {
  onClose: PropTypes.func.isRequired,
  classes: PropTypes.object.isRequired,
  theme: PropTypes.object.isRequired,
  setLoginStatus: PropTypes.func.isRequired
}

export default withStyles(styles, { withTheme: true })(ChangePassword)
