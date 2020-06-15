#ifndef DALI_OFFSCREEN_APPLICATION_H
#define DALI_OFFSCREEN_APPLICATION_H

/*
 * Copyright (c) 2020 Samsung Electronics Co., Ltd.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

/**
 * @addtogroup dali_adaptor_framework
 * @{
 */

// EXTERNAL INCLUDES
#include <dali/public-api/signals/dali-signal.h>
#include <dali/public-api/object/any.h>

namespace Dali
{

class OffscreenWindow;

namespace Internal
{
class OffscreenApplication;
}

/**
 * @brief Appliations can draw UI on offscreen surface with the OffscreenApplication.
 * When you use a OffscreenApplication, you don't have to make a Window.
 */
class DALI_IMPORT_API OffscreenApplication : public Dali::BaseHandle
{
public:

  typedef Signal<void (void)> OffscreenApplicationSignalType;

public:

  /**
   * @brief This is the constructor of OffscreenApplication
   *
   * @param[in] width The initial width of the default OffscreenWindow
   * @param[in] height The initial height of the default OffscreenWindow
   * @param[in] isTranslucent Whether the OffscreenWindow is translucent or not
   */
  static OffscreenApplication New( uint16_t width, uint16_t height, bool isTranslucent );

  /**
   * @brief This is the constructor of OffscreenApplication
   *
   * @param[in] surface The native surface handle to create the OffscreenWindow
   * @param[in] isTranslucent Whether the OffscreenWindow is translucent or not
   */
  static OffscreenApplication New( Dali::Any surface, bool isTranslucent );

  /**
   * @brief Constructs an empty handle
   */
 OffscreenApplication();

  /**
   * @brief Copy constructor
   */
 OffscreenApplication( const OffscreenApplication& offscreenApplication );

  /**
   * @brief Assignment operator
   */
 OffscreenApplication& operator=( const OffscreenApplication& offscreenApplication );

  /**
   * @brief Destructor
   */
   ~OffscreenApplication();

public:

  /**
   * @brief Runs the OffscreenApplication (rendering, event handling, etc)
   */
  void Run();

  /**
   * @brief Stops the OffscreenApplication
   */
  void Stop();


  /**
   * @brief Get the default Window handle
   * @return The default Window
   */
  OffscreenWindow GetWindow();

public:  // Signals

  /**
   * @brief Signal to notify the client when the application is ready to be initialized
   *
   * @note OffscreenApplication::Run() should be called to be initialized
   *
   * @return The signal
   */
 OffscreenApplicationSignalType& InitSignal();

  /**
   * @brief Signal to notify the user when the application is about to be terminated
   *
   * @return The signal
   */
 OffscreenApplicationSignalType& TerminateSignal();

public: // Not intended for application developers
  /**
   * @brief Internal constructor
   */
  explicit DALI_INTERNAL OffscreenApplication( Internal::OffscreenApplication* offscreenApplication );

};

/**
 * @}
 */

}  // namespace Dali

#endif // DALI_OFFSCREEN_APPLICATION_H