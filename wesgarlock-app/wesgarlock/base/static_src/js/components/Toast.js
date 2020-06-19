import React from 'react'
import PropTypes from 'prop-types'
import { Snackbar, Typography } from '@material-ui/core'
import { Alert } from '@material-ui/lab'
import Slide from '@material-ui/core/Slide'

function TransitionDown (props) {
  return <Slide {...props} direction="down" />
}

function Toast (props) {
  const {
    message,
    duration,
    open,
    handleClose,
    severity
  } = props

  return (
        <Snackbar
            open={open}
            autoHideDuration={duration || 6000}
            onClose={handleClose}
            TransitionComponent={TransitionDown}
            anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
            >
            <Alert onClose={handleClose} severity={severity}>
                <Typography>
                    {message || 'no message supplier'}
                </Typography>
            </Alert>
        </Snackbar>
  )
}

Toast.propTypes = {
  message: PropTypes.string.isRequired,
  duration: PropTypes.number.isRequired,
  open: PropTypes.bool.isRequired,
  handleClose: PropTypes.func.isRequired,
  severity: PropTypes.string.isRequired
}

export default Toast
