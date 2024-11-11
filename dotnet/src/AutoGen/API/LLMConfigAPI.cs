﻿// Copyright (c) 2023 - 2024, Owners of https://github.com/ag2labs
// SPDX-License-Identifier: Apache-2.0
// Contributions to this project, i.e., https://github.com/ag2labs/ag2, 
// are licensed under the Apache License, Version 2.0 (Apache-2.0).
// Portions derived from  https://github.com/microsoft/autogen under the MIT License.
// SPDX-License-Identifier: MIT
// Copyright (c) Microsoft Corporation. All rights reserved.
// LLMConfigAPI.cs

using System;
using System.Collections.Generic;
using System.Linq;
using AutoGen.OpenAI.V1;

namespace AutoGen
{
    public static class LLMConfigAPI
    {
        public static IEnumerable<ILLMConfig> GetOpenAIConfigList(
            string apiKey,
            IEnumerable<string>? modelIDs = null)
        {
            var models = modelIDs ?? new[]
            {
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-16k",
                "gpt-4",
                "gpt-4-32k",
                "gpt-4-0613",
                "gpt-4-32k-0613",
                "gpt-4-1106-preview",
            };

            return models.Select(modelId => new OpenAIConfig(apiKey, modelId));
        }

        public static IEnumerable<ILLMConfig> GetAzureOpenAIConfigList(
            string endpoint,
            string apiKey,
            IEnumerable<string> deploymentNames)
        {
            return deploymentNames.Select(deploymentName => new AzureOpenAIConfig(endpoint, deploymentName, apiKey));
        }

        /// <summary>
        /// Get a list of LLMConfig objects from a JSON file.
        /// </summary>
        internal static IEnumerable<ILLMConfig> ConfigListFromJson(
            string filePath,
            IEnumerable<string>? filterModels = null)
        {
            // Disable this API from documentation for now.
            throw new NotImplementedException();
        }
    }
}
