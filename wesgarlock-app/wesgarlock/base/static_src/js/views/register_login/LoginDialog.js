/* global context */

import React, { useState, useRef, Fragment } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import {
  TextField,
  Button,
  Checkbox,
  Typography,
  FormControlLabel,
  withStyles
} from '@material-ui/core'
import ActionFormDialog from '../../components/ActionFormDialog'
import HighlightedInformation from '../../components/HighlightedInformation'
import ButtonCircularProgress from '../../components/ButtonCircularProgress'
import VisibilityPasswordTextField from '../../components/VisibilityPasswordTextField'

const styles = (theme) => ({
  forgotPassword: {
    marginTop: theme.spacing(2),
    color: theme.palette.primary.main,
    cursor: 'pointer',
    '&:enabled:hover': {
      color: theme.palette.primary.dark
    },
    '&:enabled:focus': {
      color: theme.palette.primary.dark
    }
  },
  disabledText: {
    cursor: 'auto',
    color: theme.palette.text.disabled
  },
  formControlLabel: {
    marginRight: 0
  }
})

function LoginDialog (props) {
  const {
    setStatus,
    classes,
    onClose,
    openChangePasswordDialog,
    status
  } = props
  const [isLoading, setIsLoading] = useState(false)
  const [isPasswordVisible, setIsPasswordVisible] = useState(false)
  const loginEmail = useRef()
  const loginPassword = useRef()

  const login = (e) => {
    setIsLoading(true)
  }

  return (
    <Fragment>
      <ActionFormDialog
        open
        onClose={onClose}
        loading={isLoading}
        onFormSubmit={(e) => { login(e) }}
        hideBackdrop
        headline="Login"
        content={
          <Fragment>
            <TextField
              variant="outlined"
              margin="normal"
              error={status === 'invalidEmail'}
              required
              fullWidth
              label="Email Address"
              inputRef={loginEmail}
              autoFocus
              autoComplete="off"
              type="email"
              name="username"
              onChange={() => {
                if (status === 'invalidEmail') {
                  setStatus(null)
                }
              }}
              helperText={
                status === 'invalidEmail' &&
                "This email address isn't associated with an account."
              }
              FormHelperTextProps={{ error: true }}
            />
            <VisibilityPasswordTextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              error={status === 'invalidPassword'}
              label="Password"
              name="password"
              inputRef={loginPassword}
              autoComplete="off"
              onChange={() => {
                if (status === 'invalidPassword') {
                  setStatus(null)
                }
              }}
              helperText={
                status === 'invalidPassword'
                  ? (
                  <span>
                    Incorrect password. Try again, or click on{' '}
                    <b>&quot;Forgot Password?&quot;</b> to reset it.
                  </span>
                    )
                  : (
                      ''
                    )
              }
              FormHelperTextProps={{ error: true }}
              onVisibilityChange={setIsPasswordVisible}
              isVisible={isPasswordVisible}
            />
            <FormControlLabel
              className={classes.formControlLabel}
              control={<Checkbox color="primary" />}
              label={<Typography variant="body1">Remember me</Typography>}
              name="rememberMe"
            />
            {status === 'verificationEmailSend'
              ? (
              <HighlightedInformation>
                We have send instructions on how to reset your password to your
                email address
              </HighlightedInformation>
                )
              : (
              <div></div>
                )}
          </Fragment>
        }
        actions={
          <Fragment>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="secondary"
              disabled={isLoading}
              size="large"
            >
              Login
              {isLoading && <ButtonCircularProgress />}
            </Button>
            <Typography
              align="center"
              className={classNames(
                classes.forgotPassword,
                isLoading ? classes.disabledText : null
              )}
              color="primary"
              onClick={isLoading ? null : openChangePasswordDialog}
              tabIndex={0}
              role="button"
              onKeyDown={(event) => {
                // For screenreaders listen to space and enter events
                if (
                  (!isLoading && event.keyCode === 13) ||
                  event.keyCode === 32
                ) {
                  openChangePasswordDialog()
                }
              }}
            >
              Forgot Password?
            </Typography>
          </Fragment>
        }
        actionUrl={context.front_urls.front_login}
        method="POST"
      />
    </Fragment>
  )
}

LoginDialog.propTypes = {
  classes: PropTypes.object.isRequired,
  onClose: PropTypes.func.isRequired,
  setStatus: PropTypes.func.isRequired,
  openChangePasswordDialog: PropTypes.func.isRequired,
  history: PropTypes.object.isRequired,
  status: PropTypes.string
}

export default withStyles(styles)(LoginDialog)
